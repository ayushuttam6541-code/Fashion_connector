import jwt
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from config.database import users
from utils.security import verify_password
import os

security = HTTPBearer()
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = "HS256"

async def get_current_user(request: Request) -> dict:
    """Get current authenticated user from JWT token"""
    # Try to get token from cookie first
    token = request.cookies.get("access_token")
    
    # If not in cookie, try Authorization header
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await users.find_one({"id": user_id})
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Remove sensitive data
        user.pop("_id", None)
        user.pop("password_hash", None)
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(*allowed_roles):
    """Dependency to check if user has required role"""
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Access forbidden. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

def require_seller_shop_access(current_user: dict = Depends(get_current_user)):
    """Ensure seller can only access their own shop data"""
    if current_user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can access this resource")
    return current_user

async def check_shop_ownership(shop_id: str, current_user: dict) -> bool:
    """Check if current user owns the specified shop"""
    from config.database import shops
    
    if current_user.get("role") == "admin":
        return True
    
    if current_user.get("role") == "seller":
        shop = await shops.find_one({"id": shop_id})
        if shop and shop.get("seller_id") == current_user.get("id"):
            return True
    
    return False

async def check_product_ownership(product_id: str, current_user: dict) -> bool:
    """Check if current user owns the specified product"""
    from config.database import products, shops
    
    if current_user.get("role") == "admin":
        return True
    
    if current_user.get("role") == "seller":
        product = await products.find_one({"id": product_id})
        if product:
            shop = await shops.find_one({"id": product.get("shop_id")})
            if shop and shop.get("seller_id") == current_user.get("id"):
                return True
    
    return False