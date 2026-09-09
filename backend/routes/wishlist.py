from fastapi import APIRouter, HTTPException, Depends
from models.schemas import WishlistItem
from middleware.auth import get_current_user, require_role
from config.database import wishlist, products
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["Wishlist"])

@router.get("", response_model=list)
async def get_wishlist(current_user: dict = Depends(get_current_user)):
    """Get user's wishlist"""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can have wishlist")
    
    wishlist_items = await wishlist.find(
        {"user_id": current_user["id"]},
        {"_id": 0}
    ).to_list(100)
    
    # Get product details for each item
    product_ids = [item["product_id"] for item in wishlist_items]
    products_list = []
    
    if product_ids:
        products_cursor = products.find({"id": {"$in": product_ids}}, {"_id": 0})
        async for product in products_cursor:
            products_list.append(product)
    
    # Combine wishlist items with product details
    result = []
    product_map = {p["id"]: p for p in products_list}
    
    for item in wishlist_items:
        product = product_map.get(item["product_id"])
        if product:
            result.append({
                **product,
                "added_at": item["created_at"]
            })
    
    return result

@router.post("", response_model=dict)
async def add_to_wishlist(
    item: WishlistItem,
    current_user: dict = Depends(require_role("customer"))
):
    """Add product to wishlist"""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can add to wishlist")
    
    # Check if product exists
    product = await products.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if already in wishlist
    existing = await wishlist.find_one({
        "user_id": current_user["id"],
        "product_id": item.product_id
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
    
    wishlist_item = {
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "product_id": item.product_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await wishlist.insert_one(wishlist_item)
    
    return {"message": "Added to wishlist successfully"}

@router.delete("/{product_id}")
async def remove_from_wishlist(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove product from wishlist"""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can manage wishlist")
    
    result = await wishlist.delete_one({
        "user_id": current_user["id"],
        "product_id": product_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
    
    return {"message": "Removed from wishlist successfully"}

@router.get("/check/{product_id}")
async def check_in_wishlist(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Check if product is in user's wishlist"""
    if current_user["role"] != "customer":
        return {"in_wishlist": False}
    
    item = await wishlist.find_one({
        "user_id": current_user["id"],
        "product_id": product_id
    })
    
    return {"in_wishlist": item is not None}