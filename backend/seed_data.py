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

# Fashion Hub seed data (real shop)
FASHION_HUB = {
    "name": "Fashion Hub",
    "category": "Readymade Garment Retailer",
    "description": "Premium readymade garments for men, women, and kids. Quality clothing at affordable prices.",
    "address": "Shop No. F-7, Gorakhnath Complex, Opposite Bikaner Sweets, East Boring Canal Road, Boring Road, Patna, Bihar 800001",
    "short_address": "East Boring Canal Road, Rajapur, Patna, Bihar 800001",
    "plus_code": "J4CG+RQ Patna, Bihar",
    "phone": "8540846184",
    "latitude": 25.6093,
    "longitude": 85.8245,
    "logo_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800",
    "banner_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200",
    "timings": {
        "Monday": "11:00 AM - 10:00 PM",
        "Tuesday": "11:00 AM - 10:00 PM",
        "Wednesday": "11:00 AM - 10:00 PM",
        "Thursday": "11:00 AM - 10:00 PM",
        "Friday": "11:00 AM - 10:00 PM",
        "Saturday": "11:00 AM - 10:00 PM",
        "Sunday": "11:00 AM - 10:00 PM"
    },
    "services": ["Readymade Garments", "Men's Clothing", "Kids Clothing", "Boutique", "Dress Materials", "Ethnic Wear"]
}

# Fictional Patna shops for demo
PATNA_SHOPS = [
    {
        "name": "Style Point",
        "category": "Men's Fashion",
        "description": "Trendy men's clothing and accessories",
        "address": "Frazer Road, Patna, Bihar 800001",
        "short_address": "Frazer Road, Patna",
        "plus_code": "J4VH+8P Patna, Bihar",
        "phone": "9876543210",
        "latitude": 25.6128,
        "longitude": 85.8250,
        "logo_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        "banner_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200",
        "timings": {
            "Monday": "10:00 AM - 9:00 PM",
            "Tuesday": "10:00 AM - 9:00 PM",
            "Wednesday": "10:00 AM - 9:00 PM",
            "Thursday": "10:00 AM - 9:00 PM",
            "Friday": "10:00 AM - 9:00 PM",
            "Saturday": "10:00 AM - 9:30 PM",
            "Sunday": "11:00 AM - 8:00 PM"
        },
        "services": ["Men's Clothing", "Formal Wear", "Casual Wear"]
    },
    {
        "name": "Trend Wear",
        "category": "Women's Fashion",
        "description": "Latest women's fashion and ethnic wear",
        "address": "Kankarbagh, Patna, Bihar 800020",
        "short_address": "Kankarbagh, Patna",
        "plus_code": "J4QJ+2R Patna, Bihar",
        "phone": "9876543211",
        "latitude": 25.6150,
        "longitude": 85.8300,
        "logo_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800",
        "banner_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=1200",
        "timings": {
            "Monday": "10:30 AM - 8:30 PM",
            "Tuesday": "10:30 AM - 8:30 PM",
            "Wednesday": "10:30 AM - 8:30 PM",
            "Thursday": "10:30 AM - 8:30 PM",
            "Friday": "10:30 AM - 8:30 PM",
            "Saturday": "10:00 AM - 9:00 PM",
            "Sunday": "Closed"
        },
        "services": ["Women's Clothing", "Sarees", "Kurtas", "Dresses"]
    },
    {
        "name": "Kids Corner",
        "category": "Kids Wear",
        "description": "Colorful and comfortable clothing for kids",
        "address": "Boring Road, Patna, Bihar 800001",
        "short_address": "Boring Road, Patna",
        "plus_code": "J4CG+6M Patna, Bihar",
        "phone": "9876543212",
        "latitude": 25.6080,
        "longitude": 85.8230,
        "logo_url": "https://images.unsplash.com/photo-1503943165676-7f4793d2a22e?w=800",
        "banner_url": "https://images.unsplash.com/photo-1503943165676-7f4793d2a22e?w=1200",
        "timings": {
            "Monday": "11:00 AM - 8:00 PM",
            "Tuesday": "11:00 AM - 8:00 PM",
            "Wednesday": "11:00 AM - 8:00 PM",
            "Thursday": "11:00 AM - 8:00 PM",
            "Friday": "11:00 AM - 8:00 PM",
            "Saturday": "10:00 AM - 9:00 PM",
            "Sunday": "11:00 AM - 7:00 PM"
        },
        "services": ["Kids Clothing", "Baby Wear", "School Uniforms"]
    },
    {
        "name": "Ethnic Boutique",
        "category": "Ethnic Wear",
        "description": "Traditional Indian wear for all occasions",
        "address": "Gandhi Maidan, Patna, Bihar 800001",
        "short_address": "Gandhi Maidan, Patna",
        "plus_code": "J4VF+Q3 Patna, Bihar",
        "phone": "9876543213",
        "latitude": 25.6100,
        "longitude": 85.8200,
        "logo_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800",
        "banner_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=1200",
        "timings": {
            "Monday": "10:00 AM - 9:00 PM",
            "Tuesday": "10:00 AM - 9:00 PM",
            "Wednesday": "10:00 AM - 9:00 PM",
            "Thursday": "10:00 AM - 9:00 PM",
            "Friday": "10:00 AM - 9:00 PM",
            "Saturday": "10:00 AM - 9:30 PM",
            "Sunday": "11:00 AM - 6:00 PM"
        },
        "services": ["Ethnic Wear", "Sarees", "Sherwanis", "Lehengas"]
    },
    {
        "name": "Denim Factory",
        "category": "Jeans",
        "description": "Premium denim and casual wear",
        "address": "Patliputra Colony, Patna, Bihar 800013",
        "short_address": "Patliputra Colony, Patna",
        "plus_code": "J4RG+5T Patna, Bihar",
        "phone": "9876543214",
        "latitude": 25.6200,
        "longitude": 85.8350,
        "logo_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800",
        "banner_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=1200",
        "timings": {
            "Monday": "11:00 AM - 9:00 PM",
            "Tuesday": "11:00 AM - 9:00 PM",
            "Wednesday": "11:00 AM - 9:00 PM",
            "Thursday": "11:00 AM - 9:00 PM",
            "Friday": "11:00 AM - 9:00 PM",
            "Saturday": "10:00 AM - 10:00 PM",
            "Sunday": "11:00 AM - 8:00 PM"
        },
        "services": ["Jeans", "Casual Wear", "T-Shirts"]
    },
    {
        "name": "Formal Fits",
        "category": "Men's Fashion",
        "description": "Professional and formal men's wear",
        "address": "Budhha Marg, Patna, Bihar 800001",
        "short_address": "Budhha Marg, Patna",
        "plus_code": "J4VH+2W Patna, Bihar",
        "phone": "9876543215",
        "latitude": 25.6130,
        "longitude": 85.8280,
        "logo_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800",
        "banner_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1200",
        "timings": {
            "Monday": "10:00 AM - 8:00 PM",
            "Tuesday": "10:00 AM - 8:00 PM",
            "Wednesday": "10:00 AM - 8:00 PM",
            "Thursday": "10:00 AM - 8:00 PM",
            "Friday": "10:00 AM - 8:00 PM",
            "Saturday": "10:00 AM - 9:00 PM",
            "Sunday": "Closed"
        },
        "services": ["Formal Wear", "Suits", "Shirts", "Trousers"]
    },
    {
        "name": "Fashion Fiesta",
        "category": "Women's Fashion",
        "description": "Contemporary women's fashion and accessories",
        "address": "Sri Krishna Nagar, Patna, Bihar 800001",
        "short_address": "Sri Krishna Nagar, Patna",
        "plus_code": "J4QJ+8X Patna, Bihar",
        "phone": "9876543216",
        "latitude": 25.6050,
        "longitude": 85.8220,
        "logo_url": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800",
        "banner_url": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=1200",
        "timings": {
            "Monday": "11:00 AM - 8:30 PM",
            "Tuesday": "11:00 AM - 8:30 PM",
            "Wednesday": "11:00 AM - 8:30 PM",
            "Thursday": "11:00 AM - 8:30 PM",
            "Friday": "11:00 AM - 8:30 PM",
            "Saturday": "10:00 AM - 9:00 PM",
            "Sunday": "12:00 PM - 7:00 PM"
        },
        "services": ["Women's Clothing", "Accessories", "Handbags"]
    },
    {
        "name": "Little Stars",
        "category": "Kids Wear",
        "description": "Adorable clothing for little ones",
        "address": "Kankarbagh Colony, Patna, Bihar 800020",
        "short_address": "Kankarbagh Colony, Patna",
        "plus_code": "J4QJ+4Y Patna, Bihar",
        "phone": "9876543217",
        "latitude": 25.6160,
        "longitude": 85.8320,
        "logo_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=800",
        "banner_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=1200",
        "timings": {
            "Monday": "10:30 AM - 8:00 PM",
            "Tuesday": "10:30 AM - 8:00 PM",
            "Wednesday": "10:30 AM - 8:00 PM",
            "Thursday": "10:30 AM - 8:00 PM",
            "Friday": "10:30 AM - 8:00 PM",
            "Saturday": "10:00 AM - 9:00 PM",
            "Sunday": "11:00 AM - 7:00 PM"
        },
        "services": ["Kids Clothing", "Baby Products", "Toys"]
    },
    {
        "name": "Traditional Touch",
        "category": "Ethnic Wear",
        "description": "Authentic traditional Indian clothing",
        "address": "Ashok Rajpath, Patna, Bihar 800004",
        "short_address": "Ashok Rajpath, Patna",
        "plus_code": "J4VF+7Z Patna, Bihar",
        "phone": "9876543218",
        "latitude": 25.6070,
        "longitude": 85.8190,
        "logo_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800",
        "banner_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=1200",
        "timings": {
            "Monday": "10:00 AM - 9:00 PM",
            "Tuesday": "10:00 AM - 9:00 PM",
            "Wednesday": "10:00 AM - 9:00 PM",
            "Thursday": "10:00 AM - 9:00 PM",
            "Friday": "10:00 AM - 9:00 PM",
            "Saturday": "10:00 AM - 9:30 PM",
            "Sunday": "11:00 AM - 6:00 PM"
        },
        "services": ["Ethnic Wear", "Kurtas", "Sarees", "Dupattas"]
    },
    {
        "name": "Casual Comfort",
        "category": "Men's Fashion",
        "description": "Comfortable casual wear for everyday",
        "address": "Police Colony, Patna, Bihar 800001",
        "short_address": "Police Colony, Patna",
        "plus_code": "J4VH+5A Patna, Bihar",
        "phone": "9876543219",
        "latitude": 25.6140,
        "longitude": 85.8260,
        "logo_url": "https://images.unsplash.com/photo-1523398002811-999ca8dec234?w=800",
        "banner_url": "https://images.unsplash.com/photo-1523398002811-999ca8dec234?w=1200",
        "timings": {
            "Monday": "11:00 AM - 9:00 PM",
            "Tuesday": "11:00 AM - 9:00 PM",
            "Wednesday": "11:00 AM - 9:00 PM",
            "Thursday": "11:00 AM - 9:00 PM",
            "Friday": "11:00 AM - 9:00 PM",
            "Saturday": "10:00 AM - 10:00 PM",
            "Sunday": "11:00 AM - 8:00 PM"
        },
        "services": ["Casual Wear", "T-Shirts", "Shorts", "Loungewear"]
    }
]

# Sample products for Fashion Hub
FASHION_HUB_PRODUCTS = [
    {
        "name": "Classic Black T-Shirt",
        "description": "Premium cotton black t-shirt, perfect for casual wear",
        "category": "Men's Fashion",
        "subcategory": "T-Shirts",
        "price": 599,
        "discount_price": 499,
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["Black", "Navy Blue", "Gray"],
        "stock": 50,
        "availability": True,
        "brand": "Fashion Hub",
        "size_stock": [
            {"size": "S", "stock": 10},
            {"size": "M", "stock": 15},
            {"size": "L", "stock": 12},
            {"size": "XL", "stock": 8},
            {"size": "XXL", "stock": 5}
        ]
    },
    {
        "name": "Formal White Shirt",
        "description": "Classic formal white shirt for office and events",
        "category": "Men's Fashion",
        "subcategory": "Shirts",
        "price": 899,
        "discount_price": 799,
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["White", "Light Blue"],
        "stock": 30,
        "availability": True,
        "brand": "Fashion Hub",
        "size_stock": [
            {"size": "S", "stock": 5},
            {"size": "M", "stock": 10},
            {"size": "L", "stock": 10},
            {"size": "XL", "stock": 5}
        ]
    },
    {
        "name": "Women's Kurti Set",
        "description": "Beautiful embroidered kurti with matching palazzo",
        "category": "Women's Fashion",
        "subcategory": "Kurtas",
        "price": 1299,
        "discount_price": 1099,
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Maroon", "Navy", "Teal"],
        "stock": 25,
        "availability": True,
        "brand": "Fashion Hub",
        "size_stock": [
            {"size": "S", "stock": 5},
            {"size": "M", "stock": 8},
            {"size": "L", "stock": 7},
            {"size": "XL", "stock": 5}
        ]
    },
    {
        "name": "Kids Denim Jacket",
        "description": "Stylish denim jacket for kids",
        "category": "Kids Wear",
        "subcategory": "Jackets",
        "price": 799,
        "discount_price": 699,
        "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
        "colors": ["Blue", "Black"],
        "stock": 20,
        "availability": True,
        "brand": "Fashion Hub",
        "size_stock": [
            {"size": "2-3Y", "stock": 5},
            {"size": "4-5Y", "stock": 5},
            {"size": "6-7Y", "stock": 5},
            {"size": "8-9Y", "stock": 5}
        ]
    },
    {
        "name": "Traditional Saree",
        "description": "Elegant silk saree with intricate designs",
        "category": "Ethnic Wear",
        "subcategory": "Sarees",
        "price": 2499,
        "discount_price": 1999,
        "sizes": ["Free Size"],
        "colors": ["Red", "Green", "Blue", "Pink"],
        "stock": 15,
        "availability": True,
        "brand": "Fashion Hub",
        "size_stock": [
            {"size": "Free Size", "stock": 15}
        ]
    }
]

# Categories
CATEGORIES = [
    {"name": "Men's Fashion", "description": "Clothing and accessories for men", "image_url": ""},
    {"name": "Women's Fashion", "description": "Clothing and accessories for women", "image_url": ""},
    {"name": "Kids Wear", "description": "Clothing for children and babies", "image_url": ""},
    {"name": "Ethnic Wear", "description": "Traditional Indian clothing", "image_url": ""},
    {"name": "Jeans", "description": "Denim and casual pants", "image_url": ""},
    {"name": "Shirts", "description": "Formal and casual shirts", "image_url": ""},
    {"name": "T-Shirts", "description": "Casual t-shirts and tops", "image_url": ""},
    {"name": "Dresses", "description": "Women's dresses and gowns", "image_url": ""},
    {"name": "Kurta", "description": "Traditional kurtas for men and women", "image_url": ""},
    {"name": "Sarees", "description": "Traditional Indian sarees", "image_url": ""},
    {"name": "Boutique", "description": "Designer and boutique clothing", "image_url": ""}
]

async def seed_database():
    """Seed the database with initial data"""
    print("Starting database seeding...")
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    # await users.delete_many({})
    # await shops.delete_many({})
    # await products.delete_many({})
    # await categories.delete_many({})
    
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
    for cat_data in CATEGORIES:
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
    fashion_hub_shop = await shops.find_one({"name": FASHION_HUB["name"]})
    if not fashion_hub_shop:
        shop_id = str(uuid.uuid4())
        shop_doc = {
            "id": shop_id,
            "seller_id": seller_id,
            "name": FASHION_HUB["name"],
            "category": FASHION_HUB["category"],
            "description": FASHION_HUB["description"],
            "address": FASHION_HUB["address"],
            "short_address": FASHION_HUB["short_address"],
            "plus_code": FASHION_HUB["plus_code"],
            "phone": FASHION_HUB["phone"],
            "logo_url": FASHION_HUB.get("logo_url"),
            "banner_url": FASHION_HUB.get("banner_url"),
            "latitude": FASHION_HUB["latitude"],
            "longitude": FASHION_HUB["longitude"],
            "location": {
                "type": "Point",
                "coordinates": [FASHION_HUB["longitude"], FASHION_HUB["latitude"]]
            },
            "timings": FASHION_HUB["timings"],
            "services": FASHION_HUB["services"],
            "status": "ACTIVE",
            "rating": 4.8,
            "review_count": 156,
            "verified": True,
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
    
    # Create Fashion Hub products
    for product_data in FASHION_HUB_PRODUCTS:
        existing = await products.find_one({"name": product_data["name"], "shop_id": shop_id})
        if not existing:
            product = {
                "id": str(uuid.uuid4()),
                "shop_id": shop_id,
                "shop_name": FASHION_HUB["name"],
                **product_data,
                "images": [],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await products.insert_one(product)
            print(f"[OK] Product created: {product_data['name']}")
        else:
            print(f"[OK] Product already exists: {product_data['name']}")
    
    # Create fictional Patna shops
    for shop_data in PATNA_SHOPS:
        existing_shop = await shops.find_one({"name": shop_data["name"]})
        if not existing_shop:
            # Create seller for each shop
            seller_id = str(uuid.uuid4())
            seller_email = f"{shop_data['name'].lower().replace(' ', '')}@example.com"
            
            seller = {
                "id": seller_id,
                "name": f"{shop_data['name']} Owner",
                "email": seller_email,
                "phone": shop_data["phone"],
                "password_hash": hash_password("Seller@123"),
                "role": "seller",
                "status": "APPROVED",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await users.insert_one(seller)
            
            # Create shop
            shop_id = str(uuid.uuid4())
            shop_doc = {
                "id": shop_id,
                "seller_id": seller_id,
                "name": shop_data["name"],
                "category": shop_data["category"],
                "description": shop_data["description"],
                "address": shop_data["address"],
                "short_address": shop_data["short_address"],
                "plus_code": shop_data["plus_code"],
                "phone": shop_data["phone"],
                "logo_url": shop_data.get("logo_url"),
                "banner_url": shop_data.get("banner_url"),
                "latitude": shop_data["latitude"],
                "longitude": shop_data["longitude"],
                "location": {
                    "type": "Point",
                    "coordinates": [shop_data["longitude"], shop_data["latitude"]]
                },
                "timings": shop_data["timings"],
                "services": shop_data["services"],
                "status": "ACTIVE",
                "rating": 4.0 + (hash(shop_data["name"]) % 10) / 10,
                "review_count": 10 + (hash(shop_data["name"]) % 50),
                "verified": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await shops.insert_one(shop_doc)
            await users.update_one({"id": seller_id}, {"$set": {"shop_id": shop_id}})
            
            print(f"[OK] Shop created: {shop_data['name']}")
            
            # Add some products to each shop
            for i in range(5, 10):
                product = {
                    "id": str(uuid.uuid4()),
                    "shop_id": shop_id,
                    "shop_name": shop_data["name"],
                    "name": f"{shop_data['category']} Product {i}",
                    "description": f"Quality {shop_data['category'].lower()} product",
                    "category": shop_data["category"],
                    "subcategory": "General",
                    "price": 500 + (i * 100),
                    "discount_price": None,
                    "images": [],
                    "sizes": ["S", "M", "L", "XL"],
                    "colors": ["Black", "Blue", "Red"],
                    "stock": 10 + i,
                    "availability": True,
                    "brand": shop_data["name"],
                    "size_stock": [
                        {"size": "S", "stock": 3},
                        {"size": "M", "stock": 3},
                        {"size": "L", "stock": 2},
                        {"size": "XL", "stock": 2}
                    ],
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
                await products.insert_one(product)
        else:
            print(f"[OK] Shop already exists: {shop_data['name']}")
    
    print("[OK] Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
