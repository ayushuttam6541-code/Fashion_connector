from fastapi import APIRouter, HTTPException, Depends, Query
from models.schemas import ShopCreate, ShopUpdate, ShopResponse, NearbyShopsQuery
from middleware.auth import get_current_user, require_role, check_shop_ownership
from config.database import shops
from utils.geo import haversine_distance, is_shop_open
import uuid
from datetime import datetime, timezone
from typing import Optional, List

router = APIRouter(tags=["Shops"])

@router.get("/shops", response_model=List[dict])
async def list_shops(
    category: Optional[str] = None,
    status: str = "ACTIVE",
    search: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 50
):
    """List all shops with optional filters"""
    query = {"status": status}
    
    # Build the search conditions
    search_conditions = []
    
    # Use either 'search' or 'q' parameter (frontend sends 'q')
    search_query = search or q
    
    if category and category.lower() != "all":
        # Flexible category matching - check if category field contains the filter
        # Also check services array for matching
        search_conditions.extend([
            {"category": {"$regex": category, "$options": "i"}},
            {"services": {"$regex": category, "$options": "i"}}
        ])
    
    if search_query:
        search_conditions.extend([
            {"name": {"$regex": search_query, "$options": "i"}},
            {"address": {"$regex": search_query, "$options": "i"}},
            {"services": {"$regex": search_query, "$options": "i"}},
            {"description": {"$regex": search_query, "$options": "i"}}
        ])
    
    # If we have search conditions, add them to the query
    if search_conditions:
        if len(search_conditions) == 1:
            query.update(search_conditions[0])
        else:
            query["$or"] = search_conditions
    
    shop_list = await shops.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    
    return shop_list

@router.get("/shops/nearby", response_model=List[dict])
async def get_nearby_shops(
    latitude: float = Query(..., description="Customer latitude"),
    longitude: float = Query(..., description="Customer longitude"),
    max_distance: float = Query(5.0, description="Maximum distance in km"),
    category: Optional[str] = None,
    limit: int = 20
):
    """Get nearby shops based on customer location using geospatial query"""
    # Build geo query
    geo_query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]  # MongoDB uses [lon, lat]
                },
                "$maxDistance": max_distance * 1000  # Convert km to meters
            }
        },
        "status": "ACTIVE"
    }
    
    if category and category.lower() != "all":
        geo_query["category"] = category
    
    nearby_shops = await shops.find(geo_query, {"_id": 0}).limit(limit).to_list(limit)
    
    # Calculate distance for each shop
    for shop in nearby_shops:
        shop_lat = shop.get("latitude")
        shop_lon = shop.get("longitude")
        if shop_lat and shop_lon:
            distance = haversine_distance(latitude, longitude, shop_lat, shop_lon)
            shop["distance"] = round(distance, 2)
            shop["is_open"] = is_shop_open(shop.get("timings", {}))
    
    # Sort by distance
    nearby_shops.sort(key=lambda x: x.get("distance", float("inf")))
    
    return nearby_shops

@router.get("/shops/featured", response_model=List[dict])
async def get_featured_shops(limit: int = 8):
    """Get featured/verified shops"""
    featured = await shops.find(
        {"status": "ACTIVE", "rating": {"$gte": 4.0}},
        {"_id": 0}
    ).sort("rating", -1).limit(limit).to_list(limit)
    
    return featured

@router.get("/shops/mine", response_model=dict)
async def get_my_shop(current_user: dict = Depends(require_role("seller"))):
    """Get current seller's shop"""
    shop = await shops.find_one(
        {"seller_id": current_user["id"]},
        {"_id": 0}
    )
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    return shop

@router.get("/shops/{shop_id}", response_model=dict)
async def get_shop(shop_id: str, latitude: Optional[float] = None, longitude: Optional[float] = None):
    """Get shop details by ID"""
    shop = await shops.find_one({"id": shop_id}, {"_id": 0})
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    # Calculate distance if customer location provided
    if latitude is not None and longitude is not None:
        shop_lat = shop.get("latitude")
        shop_lon = shop.get("longitude")
        if shop_lat and shop_lon:
            distance = haversine_distance(latitude, longitude, shop_lat, shop_lon)
            shop["distance"] = round(distance, 2)
    
    # Check if shop is currently open
    shop["is_open"] = is_shop_open(shop.get("timings", {}))
    
    return shop

@router.post("/shops", response_model=dict)
async def create_shop(shop_data: ShopCreate, current_user: dict = Depends(require_role("seller"))):
    """Create a new shop for the current seller"""
    # Check if seller already has a shop
    existing_shop = await shops.find_one({"seller_id": current_user["id"]})
    if existing_shop:
        raise HTTPException(status_code=400, detail="Seller already has a registered shop")
    
    shop_id = str(uuid.uuid4())
    
    # Create location object for geospatial queries
    location = {
        "type": "Point",
        "coordinates": [shop_data.longitude, shop_data.latitude]  # [lon, lat]
    }
    
    shop_doc = {
        "id": shop_id,
        "seller_id": current_user["id"],
        "name": shop_data.name,
        "category": shop_data.category,
        "description": shop_data.description,
        "address": shop_data.address,
        "short_address": shop_data.short_address,
        "plus_code": shop_data.plus_code,
        "phone": shop_data.phone,
        "logo_url": shop_data.logo_url,
        "banner_url": shop_data.banner_url,
        "latitude": shop_data.latitude,
        "longitude": shop_data.longitude,
        "location": location,
        "timings": shop_data.timings,
        "services": shop_data.services,
        "status": "PENDING",  # Requires admin approval
        "rating": 0.0,
        "review_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await shops.insert_one(shop_doc)
    
    # Update user with shop_id
    from backend.config.database import users
    await users.update_one(
        {"id": current_user["id"]},
        {"$set": {"shop_id": shop_id}}
    )
    
    shop_doc.pop("_id", None)
    return shop_doc

@router.put("/shops/{shop_id}", response_model=dict)
async def update_shop(
    shop_id: str,
    shop_data: ShopUpdate,
    current_user: dict = Depends(require_role("seller", "admin"))
):
    """Update shop details"""
    # Check ownership
    if not await check_shop_ownership(shop_id, current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to update this shop")
    
    # Build update data
    update_data = shop_data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # If location is updated, update the geospatial location field
    if "latitude" in update_data or "longitude" in update_data:
        current_shop = await shops.find_one({"id": shop_id})
        lat = update_data.get("latitude", current_shop.get("latitude"))
        lon = update_data.get("longitude", current_shop.get("longitude"))
        update_data["location"] = {
            "type": "Point",
            "coordinates": [lon, lat]
        }
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await shops.update_one({"id": shop_id}, {"$set": update_data})
    
    updated_shop = await shops.find_one({"id": shop_id}, {"_id": 0})
    return updated_shop

@router.delete("/shops/{shop_id}")
async def delete_shop(shop_id: str, current_user: dict = Depends(require_role("admin"))):
    """Delete a shop (admin only)"""
    shop = await shops.find_one({"id": shop_id})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    await shops.delete_one({"id": shop_id})
    
    # Update user
    from backend.config.database import users
    await users.update_one(
        {"shop_id": shop_id},
        {"$set": {"shop_id": None}}
    )
    
    return {"message": "Shop deleted successfully"}