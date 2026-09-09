import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(Path(__file__).parent)

from config.database import users, shops, products, categories
from utils.security import hash_password
import uuid
from datetime import datetime, timezone

async def seed_database():
    """Simple database seeding without unicode characters"""
    print("Starting database seeding...")
    
    # Create admin user
    admin_id = str(uuid.uuid4())
    admin_email = "ayushuttam6541@gmail.com"
    admin_password = "Admin@Fashion2026"
    
    existing_admin = await users.find_one({"email": admin_email})
    if not existing_admin:
        admin_user = {
            "id": admin_id,
            "name": "Admin",
            "email": admin_email,
            "password_hash": hash_password(admin_password),
            "role": "admin",
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await users.insert_one(admin_user)
        print(f"[OK] Admin user created: {admin_email}")
    else:
        print(f"[OK] Admin user already exists: {admin_email}")
    
    # Create categories
    category_list = [
        {"name": "Men's Fashion", "description": "Clothing for men"},
        {"name": "Women's Fashion", "description": "Clothing for women"},
        {"name": "Kids Wear", "description": "Children's clothing"},
        {"name": "Ethnic Wear", "description": "Traditional Indian wear"}
    ]
    
    for cat_data in category_list:
        existing = await categories.find_one({"name": cat_data["name"]})
        if not existing:
            category = {
                "id": str(uuid.uuid4()),
                **cat_data,
                "product_count": 0,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await categories.insert_one(category)
            print(f"[OK] Category created: {cat_data['name']}")
        else:
            print(f"[OK] Category already exists: {cat_data['name']}")
    
    # Create Fashion Hub seller and shop
    fashion_hub_seller_email = "fashionhub@example.com"
    fashion_hub_seller = await users.find_one({"email": fashion_hub_seller_email})
    
    if not fashion_hub_seller:
        seller_id = str(uuid.uuid4())
        seller = {
            "id": seller_id,
            "name": "Fashion Hub Owner",
            "email": fashion_hub_seller_email,
            "phone": "8540846184",
            "password_hash": hash_password("Seller@123"),
            "role": "seller",
            "status": "APPROVED",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await users.insert_one(seller)
        print(f"[OK] Fashion Hub seller created")
        fashion_hub_seller = seller
    else:
        print(f"[OK] Fashion Hub seller already exists")
        seller_id = fashion_hub_seller["id"]
    
    # Create Fashion Hub shop
    fashion_hub_shop = await shops.find_one({"name": "Fashion Hub"})
    if not fashion_hub_shop:
        shop_id = str(uuid.uuid4())
        shop_doc = {
            "id": shop_id,
            "seller_id": seller_id,
            "name": "Fashion Hub",
            "category": "Readymade Garment Retailer",
            "description": "Premium readymade garments for men, women, and kids",
            "address": "Shop No. F-7, Gorakhnath Complex, Opposite Bikaner Sweets, East Boring Canal Road, Boring Road, Patna, Bihar 800001",
            "short_address": "East Boring Canal Road, Rajapur, Patna, Bihar 800001",
            "plus_code": "J4CG+RQ Patna, Bihar",
            "phone": "8540846184",
            "logo_url": None,
            "banner_url": None,
            "latitude": 25.6093,
            "longitude": 85.8245,
            "location": {
                "type": "Point",
                "coordinates": [85.8245, 25.6093]
            },
            "timings": {
                "Monday": "11:00 AM - 10:00 PM",
                "Tuesday": "11:00 AM - 10:00 PM",
                "Wednesday": "11:00 AM - 10:00 PM",
                "Thursday": "11:00 AM - 10:00 PM",
                "Friday": "11:00 AM - 10:00 PM",
                "Saturday": "11:00 AM - 10:00 PM",
                "Sunday": "11:00 AM - 10:00 PM"
            },
            "services": ["Readymade Garments", "Men's Clothing", "Kids Clothing"],
            "status": "ACTIVE",
            "rating": 4.8,
            "review_count": 156,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await shops.insert_one(shop_doc)
        await users.update_one({"id": seller_id}, {"$set": {"shop_id": shop_id}})
        print(f"[OK] Fashion Hub shop created")
        fashion_hub_shop = shop_doc
    else:
        print(f"[OK] Fashion Hub shop already exists")
        shop_id = fashion_hub_shop["id"]
    
    # Create sample products
    sample_products = [
        {
            "name": "Classic Black T-Shirt",
            "description": "Premium cotton black t-shirt",
            "category": "Men's Fashion",
            "price": 599,
            "sizes": ["S", "M", "L", "XL"],
            "stock": 50
        },
        {
            "name": "Women's Kurta",
            "description": "Beautiful embroidered kurti",
            "category": "Women's Fashion", 
            "price": 899,
            "sizes": ["S", "M", "L"],
            "stock": 30
        }
    ]
    
    for product_data in sample_products:
        existing = await products.find_one({"name": product_data["name"], "shop_id": shop_id})
        if not existing:
            product = {
                "id": str(uuid.uuid4()),
                "shop_id": shop_id,
                "shop_name": "Fashion Hub",
                **product_data,
                "images": [],
                "availability": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await products.insert_one(product)
            print(f"[OK] Product created: {product_data['name']}")
        else:
            print(f"[OK] Product already exists: {product_data['name']}")
    
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())