from fastapi import APIRouter, HTTPException, Depends
from models.schemas import OrderCreate, OrderStatusUpdate, OrderResponse
from middleware.auth import get_current_user, require_role
from config.database import orders, products, shops, users, cart
import uuid
from datetime import datetime, timezone
from typing import List

router = APIRouter(tags=["Orders"])

@router.post("", response_model=dict)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(require_role("customer"))
):
    """Create a new order"""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create orders")
    
    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    
    # Validate all items and calculate totals
    order_items = []
    shop_id = None
    subtotal = 0.0
    
    for item in order_data.items:
        product = await products.find_one({"id": item.product_id})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found: {item.product_id}")
        
        if not product["availability"]:
            raise HTTPException(status_code=400, detail=f"Product not available: {product['name']}")
        
        # Check stock
        if product["stock"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for: {product['name']}")
        
        # Check that all items are from the same shop (for MVP)
        if shop_id is None:
            shop_id = product["shop_id"]
        elif product["shop_id"] != shop_id:
            raise HTTPException(status_code=400, detail="All items must be from the same shop")
        
        # Validate size/color if specified
        if item.size and item.size not in product["sizes"]:
            raise HTTPException(status_code=400, detail=f"Invalid size for: {product['name']}")
        
        if item.color and item.color not in product["colors"]:
            raise HTTPException(status_code=400, detail=f"Invalid color for: {product['name']}")
        
        item_total = product["price"] * item.quantity
        subtotal += item_total
        
        order_items.append({
            "product_id": item.product_id,
            "name": product["name"],
            "price": product["price"],
            "quantity": item.quantity,
            "size": item.size,
            "color": item.color,
            "shop_id": product["shop_id"]
        })
    
    # Validate shop
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if shop.get("status") != "ACTIVE":
        raise HTTPException(status_code=400, detail="Shop is not active")
    
    # Calculate delivery fee
    delivery_fee = 0.0 if order_data.fulfillment_type == "STORE_PICKUP" else 50.0
    total = subtotal + delivery_fee
    
    # Create order
    order_id = str(uuid.uuid4())
    
    order_doc = {
        "id": order_id,
        "customer_id": current_user["id"],
        "customer_email": current_user["email"],
        "customer_name": current_user["name"],
        "items": order_items,
        "shop_id": shop_id,
        "shop_name": shop["name"],
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "status": "PENDING",
        "payment_status": "PENDING",
        "fulfillment_type": order_data.fulfillment_type,
        "shipping_address": order_data.shipping_address,
        "customer_notes": order_data.customer_notes,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await orders.insert_one(order_doc)
    
    # Update product stock
    for item in order_items:
        await products.update_one(
            {"id": item["product_id"]},
            {"$inc": {"stock": -item["quantity"]}}
        )
    
    # Clear cart items that were ordered
    for item in order_data.items:
        await cart.delete_many({
            "user_id": current_user["id"],
            "product_id": item.product_id
        })
    
    order_doc.pop("_id", None)
    return order_doc

@router.get("", response_model=List[dict])
async def get_orders(
    status: str = None,
    current_user: dict = Depends(get_current_user)
):
    """Get orders for current user"""
    query = {}
    
    if current_user["role"] == "customer":
        query["customer_id"] = current_user["id"]
    elif current_user["role"] == "seller":
        # Get seller's shop
        shop = await shops.find_one({"seller_id": current_user["id"]})
        if shop:
            query["shop_id"] = shop["id"]
        else:
            return []
    elif current_user["role"] == "admin":
        pass  # Admin can see all orders
    else:
        raise HTTPException(status_code=403, detail="Invalid role")
    
    if status:
        query["status"] = status
    
    order_list = await orders.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    return order_list

@router.get("/{order_id}", response_model=dict)
async def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """Get order details"""
    order = await orders.find_one({"id": order_id}, {"_id": 0})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check access permissions
    if current_user["role"] == "customer":
        if order["customer_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user["role"] == "seller":
        shop = await shops.find_one({"seller_id": current_user["id"]})
        if not shop or order["shop_id"] != shop["id"]:
            raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    return order

@router.put("/{order_id}/status", response_model=dict)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    current_user: dict = Depends(require_role("seller", "admin"))
):
    """Update order status"""
    order = await orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permissions
    if current_user["role"] == "seller":
        shop = await shops.find_one({"seller_id": current_user["id"]})
        if not shop or order["shop_id"] != shop["id"]:
            raise HTTPException(status_code=403, detail="You can only update orders for your shop")
    
    # Validate status transition
    valid_statuses = ["PENDING", "ACCEPTED", "REJECTED", "PREPARING", "READY_FOR_PICKUP", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    # Update order
    await orders.update_one(
        {"id": order_id},
        {"$set": {
            "status": status_update.status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    # If order is cancelled, restore stock
    if status_update.status == "CANCELLED":
        for item in order["items"]:
            await products.update_one(
                {"id": item["product_id"]},
                {"$inc": {"stock": item["quantity"]}}
            )
    
    updated_order = await orders.find_one({"id": order_id}, {"_id": 0})
    return updated_order

@router.put("/{order_id}/payment-status")
async def update_payment_status(
    order_id: str,
    payment_data: dict,
    current_user: dict = Depends(require_role("admin"))
):
    """Update payment status (admin only)"""
    order = await orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    payment_status = payment_data.get("payment_status")
    valid_statuses = ["PENDING", "PAID", "FAILED", "REFUNDED"]
    
    if payment_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid payment status")
    
    await orders.update_one(
        {"id": order_id},
        {"$set": {
            "payment_status": payment_status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    return {"message": "Payment status updated successfully"}