from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

# User Models
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class UserRegister(UserBase):
    password: str = Field(min_length=6)
    role: str = "customer"  # customer | seller | admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    status: str
    phone: Optional[str] = None
    shop_id: Optional[str] = None
    created_at: datetime

# Shop Models
class ShopLocation(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [longitude, latitude]

class ShopTiming(BaseModel):
    Monday: str
    Tuesday: str
    Wednesday: str
    Thursday: str
    Friday: str
    Saturday: str
    Sunday: str

class ShopBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = ""
    address: str
    short_address: Optional[str] = ""
    plus_code: Optional[str] = ""
    phone: str
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    latitude: float
    longitude: float
    timings: Dict[str, str]
    services: List[str] = []

class ShopCreate(ShopBase):
    pass

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    short_address: Optional[str] = None
    plus_code: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timings: Optional[Dict[str, str]] = None
    services: Optional[List[str]] = None

class ShopResponse(BaseModel):
    id: str
    seller_id: str
    name: str
    category: str
    description: str
    address: str
    short_address: str
    plus_code: str
    phone: str
    logo_url: Optional[str]
    banner_url: Optional[str]
    latitude: float
    longitude: float
    timings: Dict[str, str]
    services: List[str]
    status: str
    rating: float
    review_count: int
    distance: Optional[float] = None  # Calculated distance from user
    created_at: datetime
    updated_at: datetime

# Product Models
class SizeStock(BaseModel):
    size: str
    stock: int

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = ""
    category: str
    subcategory: Optional[str] = ""
    price: float = Field(gt=0)
    discount_price: Optional[float] = None
    images: List[str] = []
    sizes: List[str] = ["S", "M", "L", "XL", "XXL"]
    colors: List[str] = []
    stock: int = Field(default=0, ge=0)
    availability: bool = True
    brand: Optional[str] = ""
    size_stock: Optional[List[SizeStock]] = []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    images: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    stock: Optional[int] = None
    availability: Optional[bool] = None
    brand: Optional[str] = None
    size_stock: Optional[List[SizeStock]] = None

class ProductResponse(BaseModel):
    id: str
    shop_id: str
    shop_name: str
    name: str
    description: str
    category: str
    subcategory: str
    price: float
    discount_price: Optional[float]
    images: List[str]
    sizes: List[str]
    colors: List[str]
    stock: int
    availability: bool
    brand: str
    size_stock: List[SizeStock]
    distance: Optional[float] = None  # Distance from user
    created_at: datetime
    updated_at: datetime

# Category Models
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = ""
    image_url: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: str
    product_count: int = 0
    created_at: datetime

# Wishlist Models
class WishlistItem(BaseModel):
    product_id: str

# Cart Models
class CartItem(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)
    size: Optional[str] = None
    color: Optional[str] = None

class CartUpdate(BaseModel):
    quantity: int = Field(ge=1)
    size: Optional[str] = None
    color: Optional[str] = None

# Order Models
class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None
    shop_id: str

class OrderCreate(BaseModel):
    items: List[OrderItem]
    fulfillment_type: str = "STORE_PICKUP"  # STORE_PICKUP | DELIVERY
    shipping_address: Optional[str] = None
    customer_notes: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str  # PENDING, ACCEPTED, REJECTED, PREPARING, READY_FOR_PICKUP, OUT_FOR_DELIVERY, DELIVERED, CANCELLED

class OrderResponse(BaseModel):
    id: str
    customer_id: str
    customer_email: str
    customer_name: str
    items: List[OrderItem]
    shop_id: str
    subtotal: float
    delivery_fee: float
    total: float
    status: str
    payment_status: str
    fulfillment_type: str
    shipping_address: Optional[str]
    customer_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

# Location Models
class NearbyShopsQuery(BaseModel):
    latitude: float
    longitude: float
    max_distance: Optional[float] = 5.0  # km
    category: Optional[str] = None

class NearbyProductsQuery(BaseModel):
    latitude: float
    longitude: float
    max_distance: Optional[float] = 5.0  # km
    category: Optional[str] = None
    search: Optional[str] = None