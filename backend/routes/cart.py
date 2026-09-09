from fastapi import APIRouter, HTTPException, Depends
from models.schemas import CartItem, CartUpdate
from middleware.auth import get_current_user, require_role
from config.database import cart, products, shops
import uuid
from datetime import datetime, timezone
from typing import List

router = APIRouter(tags=["Cart"])

@router.get("", response_model=list)
async def get_cart(current_user: dict = Depends(get_current_user)):
    """Get user's cart"""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can have cart")
    
    cart_items = await cart.find(
        {"user_id": current_user["id"]},
        {"_id": 0}
    ).to_list(100)
    
    # Get product and shop details for each item
    result = []
    
    for item in cart_items:
        product = await products.find_one({"id": item["product_id"]}, {"_id": 0})
        if product:
            shop = await shops.find_one({"id": product["shop_id"]}, {"_id": 0})
            
            cart_item = {
                **item,
                "product": product,
                "shop": shop
            }
            result.append(cart_item)
    
    return result

@router.post("/items", response_model=dict)
async def add_to_cart(
    item: CartItem,
    current_user: dict = Depends(require_role("customer"))
):
    """Add item to cart"""
    # Check if product exists and is available
    product = await products.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product["availability"]:
        raise HTTPException(status_code=400, detail="Product is not available")
    
    # Check stock
    if product["stock"] < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Check if item size/color is valid if specified
    if item.size and item.size not in product["sizes"]:
        raise HTTPException(status_code=400, detail="Invalid size")
    
    if item.color and item.color not in product["colors"]:
        raise HTTPException(status_code=400, detail="Invalid color")
    
    # Check if item already exists in cart
    existing = await cart.find_one({
        "user_id": current_user["id"],
        "product_id": item.product_id,
        "size": item.size,
        "color": item.color
    })
    
    if existing:
        # Update quantity
        new_quantity = existing["quantity"] + item.quantity
        if new_quantity > product["stock"]:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        await cart.update_one(
            {"id": existing["id"]},
            {"$set": {
                "quantity": new_quantity,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {"message": "Cart item updated successfully"}
    
    # Add new item to cart
    cart_item = {
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "product_id": item.product_id,
        "quantity": item.quantity,
        "size": item.size,
        "color": item.color,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await cart.insert_one(cart_item)
    
    return {"message": "Added to cart successfully"}

@router.put("/items/{item_id}", response_model=dict)
async def update_cart_item(
    item_id: str,
    update_data: CartUpdate,
    current_user: dict = Depends(require_role("customer"))
):
    """Update cart item"""
    cart_item = await cart.find_one({
        "id": item_id,
        "user_id": current_user["id"]
    })
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check stock
    product = await products.find_one({"id": cart_item["product_id"]})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if update_data.quantity > product["stock"]:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Update item
    await cart.update_one(
        {"id": item_id},
        {"$set": {
            "quantity": update_data.quantity,
            "size": update_data.size,
            "color": update_data.color,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    return {"message": "Cart item updated successfully"}

@router.delete("/items/{item_id}")
async def remove_cart_item(
    item_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove item from cart"""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can manage cart")
    
    result = await cart.delete_one({
        "id": item_id,
        "user_id": current_user["id"]
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    return {"message": "Item removed from cart successfully"}

@router.delete("")
async def clear_cart(current_user: dict = Depends(require_role("customer"))):
    """Clear entire cart"""
    await cart.delete_many({"user_id": current_user["id"]})
    return {"message": "Cart cleared successfully"}