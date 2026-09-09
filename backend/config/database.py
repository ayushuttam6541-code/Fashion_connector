import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver()
dns.resolver.default_resolver.nameservers = [
    "8.8.8.8",
    "1.1.1.1"
]

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'fashionconnect_db')

# MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]

# Database collections
users = database.users
shops = database.shops
products = database.products
categories = database.categories
wishlist = database.wishlist
cart = database.cart
orders = database.orders
files = database.files
payment_transactions = database.payment_transactions
contact_messages = database.contact_messages

async def init_db():
    """Initialize database indexes"""
    try:
        # User indexes
        await users.create_index("email", unique=True)
        await users.create_index("id")
        await users.create_index("role")
        
        # Shop indexes
        await shops.create_index("id", unique=True)
        await shops.create_index("owner_id")
        await shops.create_index("status")
        await shops.create_index("category")
        # Geospatial index for location-based queries
        await shops.create_index([("location", "2dsphere")])
        
        # Product indexes
        await products.create_index("id", unique=True)
        await products.create_index("shop_id")
        await products.create_index("category")
        await products.create_index("name")
        
        # Category indexes
        await categories.create_index("name", unique=True)
        
        # Wishlist indexes
        await wishlist.create_index([("user_id", "product_id")], unique=True)
        
        # Cart indexes
        await cart.create_index("user_id")
        
        # Order indexes
        await orders.create_index("user_id")
        await orders.create_index("shop_id")
        await orders.create_index("status")
        
        # Contact message indexes
        await contact_messages.create_index("email")
        await contact_messages.create_index("created_at")
        
        print("Database indexes initialized successfully")
    except Exception as e:
        print(f"Error initializing database indexes: {e}")

async def close_db():
    """Close database connection"""
    client.close()