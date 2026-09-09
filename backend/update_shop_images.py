import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
os.chdir(Path(__file__).parent)

from config.database import shops

# Shop image updates
SHOP_IMAGE_UPDATES = {
    "Fashion Hub": {
        "logo_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800",
        "banner_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200"
    },
    "Style Point": {
        "logo_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        "banner_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200"
    },
    "Trend Wear": {
        "logo_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800",
        "banner_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=1200"
    },
    "Kids Corner": {
        "logo_url": "https://images.unsplash.com/photo-1503943165676-7f4793d2a22e?w=800",
        "banner_url": "https://images.unsplash.com/photo-1503943165676-7f4793d2a22e?w=1200"
    },
    "Ethnic Boutique": {
        "logo_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800",
        "banner_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=1200"
    },
    "Denim Factory": {
        "logo_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800",
        "banner_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=1200"
    },
    "Formal Fits": {
        "logo_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800",
        "banner_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=1200"
    },
    "Fashion Fiesta": {
        "logo_url": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800",
        "banner_url": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=1200"
    },
    "Little Stars": {
        "logo_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=800",
        "banner_url": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=1200"
    },
    "Traditional Touch": {
        "logo_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800",
        "banner_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=1200"
    },
    "Casual Comfort": {
        "logo_url": "https://images.unsplash.com/photo-1523398002811-999ca8dec234?w=800",
        "banner_url": "https://images.unsplash.com/photo-1523398002811-999ca8dec234?w=1200"
    }
}

async def update_shop_images():
    """Update existing shops with image URLs"""
    print("Starting shop image updates...")
    
    for shop_name, image_data in SHOP_IMAGE_UPDATES.items():
        shop = await shops.find_one({"name": shop_name})
        if shop:
            await shops.update_one(
                {"name": shop_name},
                {"$set": {
                    "logo_url": image_data["logo_url"],
                    "banner_url": image_data["banner_url"],
                    "verified": True
                }}
            )
            print(f"[OK] Updated images for: {shop_name}")
        else:
            print(f"[SKIP] Shop not found: {shop_name}")
    
    print("[OK] Shop image updates completed successfully!")

if __name__ == "__main__":
    asyncio.run(update_shop_images())