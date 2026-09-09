from fastapi import APIRouter, HTTPException, Depends, Query
from models.schemas import ProductCreate, ProductUpdate, ProductResponse, NearbyProductsQuery
from middleware.auth import get_current_user, require_role, check_product_ownership
from config.database import products, shops
from utils.geo import haversine_distance
import uuid
from datetime import datetime, timezone
from typing import Optional, List

router = APIRouter(tags=["Products"])

@router.get("/products", response_model=List[dict])
async def list_products(
    shop_id: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    available_only: bool = False,
    limit: int = 100
):
    """List products with optional filters"""
    query = {}
    
    if shop_id:
        query["shop_id"] = shop_id
    
    if category and category.lower() != "all":
        query["category"] = category
    
    if available_only:
        query["availability"] = True
        query["stock"] = {"$gt": 0}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"brand": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ]
    
    product_list = await products.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    return product_list

@router.get("/products/nearby", response_model=List[dict])
async def get_nearby_products(
    latitude: float = Query(..., description="Customer latitude"),
    longitude: float = Query(..., description="Customer longitude"),
    max_distance: float = Query(5.0, description="Maximum distance in km"),
    category: Optional[str] = None,
    search: Optional[str] = None,
    available_only: bool = True,
    limit: int = 50
):
    """Get nearby products based on customer location"""
    # First get nearby shops using geospatial query
    from config.database import shops
    
    geo_query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": max_distance * 1000
            }
        },
        "status": "ACTIVE"
    }
    
    if category and category.lower() != "all":
        geo_query["category"] = category
    
    nearby_shops = await shops.find(geo_query, {"_id": 0}).limit(50).to_list(50)
    
    # Calculate distance for each shop
    for shop in nearby_shops:
        shop_lat = shop.get("latitude")
        shop_lon = shop.get("longitude")
        if shop_lat and shop_lon:
            distance = haversine_distance(latitude, longitude, shop_lat, shop_lon)
            shop["distance"] = round(distance, 2)
    shop_ids = [shop["id"] for shop in nearby_shops]
    
    if not shop_ids:
        return []
    
    # Build product query
    query = {"shop_id": {"$in": shop_ids}}
    
    if category and category.lower() != "all":
        query["category"] = category
    
    if available_only:
        query["availability"] = True
        query["stock"] = {"$gt": 0}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"brand": {"$regex": search, "$options": "i"}}
        ]
    
    nearby_products = await products.find(query, {"_id": 0}).limit(limit).to_list(limit)
    
    # Add shop information and distance
    shop_map = {shop["id"]: shop for shop in nearby_shops}
    
    for product in nearby_products:
        shop = shop_map.get(product["shop_id"])
        if shop:
            product["shop_name"] = shop["name"]
            product["shop_address"] = shop["address"]
            product["shop_distance"] = shop.get("distance")
            product["shop_rating"] = shop.get("rating")
    
    # Sort by distance
    nearby_products.sort(key=lambda x: x.get("shop_distance", float("inf")))
    
    return nearby_products

@router.get("/products/{product_id}", response_model=dict)
async def get_product(product_id: str, latitude: Optional[float] = None, longitude: Optional[float] = None):
    """Get product details by ID"""
    product = await products.find_one({"id": product_id}, {"_id": 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get shop information
    shop = await shops.find_one({"id": product["shop_id"]}, {"_id": 0})
    if shop:
        product["shop_name"] = shop["name"]
        product["shop_address"] = shop["address"]
        product["shop_phone"] = shop["phone"]
        
        # Calculate distance if location provided
        if latitude is not None and longitude is not None:
            shop_lat = shop.get("latitude")
            shop_lon = shop.get("longitude")
            if shop_lat and shop_lon:
                distance = haversine_distance(latitude, longitude, shop_lat, shop_lon)
                product["distance"] = round(distance, 2)
    
    return product

@router.post("/products", response_model=dict)
async def create_product(
    product_data: ProductCreate,
    current_user: dict = Depends(require_role("seller"))
):
    """Create a new product"""
    # Get seller's shop
    shop = await shops.find_one({"seller_id": current_user["id"]})
    if not shop:
        raise HTTPException(status_code=400, detail="Register a shop first")
    
    if shop["status"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Shop must be active to add products")
    
    product_id = str(uuid.uuid4())
    
    product_doc = {
        "id": product_id,
        "shop_id": shop["id"],
        "shop_name": shop["name"],
        "name": product_data.name,
        "description": product_data.description,
        "category": product_data.category,
        "subcategory": product_data.subcategory,
        "price": product_data.price,
        "discount_price": product_data.discount_price,
        "images": product_data.images,
        "sizes": product_data.sizes,
        "colors": product_data.colors,
        "stock": product_data.stock,
        "availability": product_data.availability,
        "brand": product_data.brand,
        "size_stock": product_data.size_stock or [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await products.insert_one(product_doc)
    
    product_doc.pop("_id", None)
    return product_doc

@router.put("/products/{product_id}", response_model=dict)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: dict = Depends(require_role("seller", "admin"))
):
    """Update product details"""
    # Check ownership
    if not await check_product_ownership(product_id, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to update this product")
    
    # Build update data
    update_data = product_data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await products.update_one({"id": product_id}, {"$set": update_data})
    
    updated_product = await products.find_one({"id": product_id}, {"_id": 0})
    return updated_product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: dict = Depends(require_role("seller", "admin"))
):
    """Delete a product"""
    # Check ownership
    if not await check_product_ownership(product_id, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to delete this product")
    
    product = await products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await products.delete_one({"id": product_id})
    
    return {"message": "Product deleted successfully"}

@router.patch("/{product_id}/stock")
async def update_product_stock(
    product_id: str,
    stock_data: dict,
    current_user: dict = Depends(require_role("seller"))
):
    """Update product stock (for inventory management)"""
    # Check ownership
    product = await products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    shop = await shops.find_one({"id": product["shop_id"]})
    if not shop or shop["seller_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="You don't have permission to update this product")
    
    # Update stock
    stock = stock_data.get("stock", 0)
    size_stock = stock_data.get("size_stock", [])
    
    update_data = {
        "stock": stock,
        "size_stock": size_stock,
        "availability": stock > 0,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await products.update_one({"id": product_id}, {"$set": update_data})
    
    return {"message": "Stock updated successfully"}