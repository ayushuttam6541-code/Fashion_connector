from fastapi import APIRouter, HTTPException, Depends
from middleware.auth import require_role
from config.database import users, shops, products, orders, contact_messages
from datetime import datetime, timezone

router = APIRouter(tags=["Admin"])

@router.get("/admin/stats")
async def get_admin_stats(current_user: dict = Depends(require_role("admin"))):
    """Get admin dashboard statistics"""
    try:
        total_shops = await shops.count_documents({})
        verified_shops = await shops.count_documents({"verified": True})
        total_products = await products.count_documents({})
        total_orders = await orders.count_documents({})
        total_users = await users.count_documents({})
        new_contact_messages = await contact_messages.count_documents({"status": "new"})
        
        # Calculate revenue from orders (simplified to avoid errors)
        revenue = 0
        try:
            revenue_pipeline = [
                {"$match": {"status": "DELIVERED"}},
                {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
            ]
            revenue_result = await orders.aggregate(revenue_pipeline).to_list(1)
            if revenue_result and "total" in revenue_result[0]:
                revenue = revenue_result[0]["total"]
        except Exception:
            revenue = 0
        
        return {
            "shops": total_shops,
            "verified_shops": verified_shops,
            "products": total_products,
            "orders": total_orders,
            "users": total_users,
            "revenue": revenue,
            "new_contact_messages": new_contact_messages
        }
    except Exception as e:
        # Return default values if there's any error
        return {
            "shops": 0,
            "verified_shops": 0,
            "products": 0,
            "orders": 0,
            "users": 0,
            "revenue": 0,
            "new_contact_messages": 0
        }

@router.get("/admin/dashboard")
async def get_admin_dashboard(current_user: dict = Depends(require_role("admin"))):
    """Get admin dashboard statistics"""
    total_customers = await users.count_documents({"role": "customer"})
    total_sellers = await users.count_documents({"role": "seller"})
    pending_sellers = await users.count_documents({"role": "seller", "status": "PENDING"})
    total_shops = await shops.count_documents({})
    pending_shops = await shops.count_documents({"status": "PENDING"})
    active_shops = await shops.count_documents({"status": "ACTIVE"})
    total_products = await products.count_documents({})
    total_orders = await orders.count_documents({})
    
    return {
        "total_customers": total_customers,
        "total_sellers": total_sellers,
        "pending_sellers": pending_sellers,
        "total_shops": total_shops,
        "pending_shops": pending_shops,
        "active_shops": active_shops,
        "total_products": total_products,
        "total_orders": total_orders
    }

@router.get("/admin/sellers")
async def get_all_sellers(
    status: str = None,
    current_user: dict = Depends(require_role("admin"))
):
    """Get all sellers with optional status filter"""
    query = {"role": "seller"}
    if status:
        query["status"] = status
    
    sellers = await users.find(query, {"_id": 0, "password_hash": 0}).sort("created_at", -1).to_list(100)
    
    # Add shop information for each seller
    for seller in sellers:
        if seller.get("shop_id"):
            shop = await shops.find_one({"id": seller["shop_id"]}, {"_id": 0})
            seller["shop"] = shop
        else:
            seller["shop"] = None
    
    return sellers

@router.put("/admin/sellers/{seller_id}/approve")
async def approve_seller(
    seller_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Approve a seller account"""
    seller = await users.find_one({"id": seller_id, "role": "seller"})
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    await users.update_one(
        {"id": seller_id},
        {"$set": {"status": "APPROVED", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Seller approved successfully"}

@router.put("/admin/sellers/{seller_id}/reject")
async def reject_seller(
    seller_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Reject a seller account"""
    seller = await users.find_one({"id": seller_id, "role": "seller"})
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    await users.update_one(
        {"id": seller_id},
        {"$set": {"status": "REJECTED", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Seller rejected successfully"}

@router.put("/admin/sellers/{seller_id}/suspend")
async def suspend_seller(
    seller_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Suspend a seller account"""
    seller = await users.find_one({"id": seller_id, "role": "seller"})
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    await users.update_one(
        {"id": seller_id},
        {"$set": {"status": "SUSPENDED", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    # Also suspend their shop
    if seller.get("shop_id"):
        await shops.update_one(
            {"id": seller["shop_id"]},
            {"$set": {"status": "SUSPENDED", "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
    
    return {"message": "Seller suspended successfully"}

@router.get("/admin/shops")
async def get_all_shops(
    status: str = None,
    current_user: dict = Depends(require_role("admin"))
):
    """Get all shops with optional status filter"""
    query = {}
    if status:
        query["status"] = status
    
    shop_list = await shops.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    # Add seller information with fields expected by frontend
    for shop in shop_list:
        seller = await users.find_one({"id": shop["seller_id"]}, {"_id": 0, "password_hash": 0})
        if seller:
            shop["owner_name"] = seller.get("name", "")
            shop["email"] = seller.get("email", "")
        else:
            shop["owner_name"] = ""
            shop["email"] = ""
        
        # Ensure categories field exists (fallback to category)
        if "categories" not in shop and "category" in shop:
            shop["categories"] = [shop["category"]]
        
        # Ensure city field exists (fallback to short_address)
        if "city" not in shop and "short_address" in shop:
            shop["city"] = shop["short_address"]
        
        # Ensure verified field exists
        if "verified" not in shop:
            shop["verified"] = False
    
    return shop_list

@router.put("/admin/shops/{shop_id}/approve")
async def approve_shop(
    shop_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Approve a shop"""
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    await shops.update_one(
        {"id": shop_id},
        {"$set": {"status": "ACTIVE", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    # Also approve the seller if not already approved
    await users.update_one(
        {"id": shop["seller_id"], "role": "seller"},
        {"$set": {"status": "APPROVED", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Shop approved successfully"}

@router.put("/admin/shops/{shop_id}/reject")
async def reject_shop(
    shop_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Reject a shop"""
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    await shops.update_one(
        {"id": shop_id},
        {"$set": {"status": "REJECTED", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Shop rejected successfully"}

@router.put("/admin/shops/{shop_id}/suspend")
async def suspend_shop(
    shop_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Suspend a shop"""
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    await shops.update_one(
        {"id": shop_id},
        {"$set": {"status": "SUSPENDED", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Shop suspended successfully"}

@router.get("/products")
async def get_all_products(
    limit: int = 100,
    current_user: dict = Depends(require_role("admin"))
):
    """Get all products (admin view)"""
    product_list = await products.find({}, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    return product_list

@router.delete("/products/{product_id}")
async def admin_delete_product(
    product_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Delete any product (admin only)"""
    product = await products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await products.delete_one({"id": product_id})
    
    return {"message": "Product deleted successfully"}

@router.get("/orders")
async def get_all_orders(
    status: str = None,
    limit: int = 100,
    current_user: dict = Depends(require_role("admin"))
):
    """Get all orders (admin view)"""
    query = {}
    if status:
        query["status"] = status
    
    order_list = await orders.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    return order_list

@router.get("/customers")
async def get_all_customers(
    current_user: dict = Depends(require_role("admin"))
):
    """Get all customers"""
    customers = await users.find(
        {"role": "customer"},
        {"_id": 0, "password_hash": 0}
    ).sort("created_at", -1).to_list(100)
    
    return customers

@router.put("/admin/shops/{shop_id}/verify")
async def verify_shop(
    shop_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Verify a shop"""
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    await shops.update_one(
        {"id": shop_id},
        {"$set": {"verified": True, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Shop verified successfully"}

@router.put("/admin/shops/{shop_id}/unverify")
async def unverify_shop(
    shop_id: str,
    current_user: dict = Depends(require_role("admin"))
):
    """Unverify a shop"""
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    await shops.update_one(
        {"id": shop_id},
        {"$set": {"verified": False, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Shop unverified successfully"}

@router.get("/admin/contact-messages")
async def get_contact_messages(current_user: dict = Depends(require_role("admin"))):
    """Get all contact messages (admin only)"""
    try:
        messages = await contact_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve contact messages")

@router.put("/admin/contact-messages/{message_id}")
async def update_contact_message_status(message_id: str, status_data: dict, current_user: dict = Depends(require_role("admin"))):
    """Update contact message status (admin only)"""
    try:
        new_status = status_data.get("status")
        if new_status not in ["new", "read", "replied", "archived"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        await contact_messages.update_one(
            {"id": message_id},
            {"$set": {"status": new_status, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        
        updated_message = await contact_messages.find_one({"id": message_id}, {"_id": 0})
        return updated_message
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update message status")