from fastapi import APIRouter, HTTPException, Depends, Response
from models.schemas import UserRegister, UserLogin, UserResponse
from middleware.auth import get_current_user, require_role
from utils.security import hash_password, verify_password, create_access_token
from config.database import users
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["Authentication"])

@router.post("/auth/register", response_model=dict)
async def register(user_data: UserRegister, response: Response):
    """Register a new user (customer or seller)"""
    email = user_data.email.lower()
    
    # Check if email already exists
    existing_user = await users.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate role
    if user_data.role not in ["customer", "seller"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Create user
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "name": user_data.name,
        "email": email,
        "phone": user_data.phone,
        "password_hash": hash_password(user_data.password),
        "role": user_data.role,
        "status": "ACTIVE" if user_data.role == "customer" else "PENDING",
        "shop_id": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await users.insert_one(user_doc)
    
    # Create token
    token = create_access_token(user_id, email, user_data.role)
    
    # Set auth cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800,  # 7 days
        path="/"
    )
    
    return {
        "id": user_id,
        "email": email,
        "name": user_data.name,
        "role": user_data.role,
        "status": user_doc["status"],
        "token": token
    }

@router.post("/auth/login", response_model=dict)
async def login(credentials: UserLogin, response: Response):
    """Login user with email and password"""
    email = credentials.email.lower()
    
    user = await users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check if user is suspended
    if user.get("status") == "SUSPENDED":
        raise HTTPException(status_code=403, detail="Account is suspended")
    
    # Create token
    token = create_access_token(user["id"], email, user["role"])
    
    # Set auth cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800,
        path="/"
    )
    
    return {
        "id": user["id"],
        "email": email,
        "name": user["name"],
        "role": user["role"],
        "status": user["status"],
        "shop_id": user.get("shop_id"),
        "token": token
    }

@router.post("/auth/logout")
async def logout(response: Response):
    """Logout user"""
    response.delete_cookie("access_token", path="/")
    return {"message": "Logged out successfully"}

@router.get("/auth/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "status": current_user["status"],
        "phone": current_user.get("phone"),
        "shop_id": current_user.get("shop_id")
    }

@router.put("/auth/profile")
async def update_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    """Update user profile"""
    user_id = current_user["id"]
    
    # Fields that can be updated
    allowed_fields = ["name", "phone"]
    update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await users.update_one({"id": user_id}, {"$set": update_data})
    
    updated_user = await users.find_one({"id": user_id})
    updated_user.pop("_id", None)
    updated_user.pop("password_hash", None)
    
    return updated_user