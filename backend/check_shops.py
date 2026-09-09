import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(Path(__file__).parent)

from config.database import shops

async def check_shops():
    """Check what shops exist in database"""
    print("Checking shops in database...")
    
    all_shops = await shops.find({}, {"_id": 0}).to_list(100)
    print(f"Total shops found: {len(all_shops)}")
    
    for shop in all_shops:
        print(f"\nShop: {shop.get('name')}")
        print(f"  Status: {shop.get('status')}")
        print(f"  Category: {shop.get('category')}")
        print(f"  Logo URL: {shop.get('logo_url')}")
        print(f"  Banner URL: {shop.get('banner_url')}")
        print(f"  Verified: {shop.get('verified')}")

if __name__ == "__main__":
    asyncio.run(check_shops())