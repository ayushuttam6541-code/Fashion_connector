from fastapi import APIRouter, HTTPException, Depends
from models.schemas import CategoryBase, CategoryResponse
from middleware.auth import require_role
from config.database import categories, products
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["Categories"])

@router.get("", response_model=list)
async def get_categories():
    """Get all categories"""
    category_list = await categories.find({}, {"_id": 0}).sort("name", 1).to_list(100)
    
    # Add product count for each category
    for category in category_list:
        count = await products.count_documents({"category": category["name"]})
        category["product_count"] = count
    
    return category_list

@router.get("/{category_id}", response_model=dict)
async def get_category(category_id: str):
    """Get category by ID"""
    category = await categories.find_one({"id": category_id}, {"_id": 0})
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Add product count
    count = await products.count_documents({"category": category["name"]})
    category["product_count"] = count
    
    return category

@router.post("", response_model=dict)
async def create_category(
    category_data: CategoryBase,
    current_user: dict = Depends(require_role("admin"))
):
    """Create a new category (admin only)"""
    # Check if category already exists
    existing = await categories.find_one({"name": category_data.name})
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    category_id = str(uuid.uuid4())
    
    category_doc = {
        "id": category_id,
        "name": category_data.name,
        "description": category_data.description,
        "image_url": category_data.image_url,
        "product_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await categories.insert_one(category_doc)
    
    category_doc.pop("_id", None)
    return category_doc

@router.put("/{category_id}", response_model=dict)
async def update_category(
    category_id: str,
    category_data: CategoryBase,
    current_user: dict = Depends(require_role("admin"))
):
    """Update category (admin only)"""
    category = await categories.find_one({"id": category_id})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if new name conflicts with existing category
    if category_data.name != category["name"]:
        existing = await categories.find_one({"name": category_data.name})
        if existing:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    update_data = {
        "name": category_data.name,
        "description": category_data.description,
        "image_url": category_data.image_url
    }
    
    await categories.update_one(
        {"id": category_id},
        {"$set": update_data}
    )
    
    updated_category = await categories.find_one({"id": category_id}, {"_id": 0})
    return updated_category

@router.delete("/{category_id}")
async def delete_category(category_id: str, current_user: dict = Depends(require_role("admin"))):
    """Delete category (admin only)"""
    category = await categories.find_one({"id": category_id})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has products
    product_count = await products.count_documents({"category": category["name"]})
    if product_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete category with existing products")
    
    await categories.delete_one({"id": category_id})
    
    return {"message": "Category deleted successfully"}