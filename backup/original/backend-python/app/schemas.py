from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class ShopBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    license_key: Optional[str] = None

class ShopCreate(ShopBase):
    pass

class Shop(ShopBase):
    id: int
    status: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    role: str = "staff"
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    shop_id: int

class UserLogin(BaseModel):
    username: str
    password: str
    shop_id: Optional[int] = None  # 使shop_id变为可选

class User(UserBase):
    id: int
    shop_id: int
    status: int
    last_login: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    parent_id: int = 0
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    shop_id: int

class Category(CategoryBase):
    id: int
    shop_id: int
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    barcode: Optional[str] = None
    price: float
    cost_price: Optional[float] = None
    stock: int = 0
    unit: Optional[str] = None

class ProductCreate(ProductBase):
    shop_id: int
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int
    shop_id: int
    category_id: Optional[int] = None
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MemberBase(BaseModel):
    name: Optional[str] = None
    phone: str
    level_id: int = 1
    points: int = 0
    balance: float = 0
    birthday: Optional[datetime] = None

class MemberCreate(MemberBase):
    shop_id: int

class Member(MemberBase):
    id: int
    shop_id: int
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    total_price: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    member_id: Optional[int] = None
    discount_amount: float = 0
    payment_method: Optional[str] = None
    remark: Optional[str] = None

class OrderCreate(OrderBase):
    shop_id: int
    operator_id: int
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    shop_id: int
    order_no: str
    total_amount: float
    payment_status: int
    status: int
    operator_id: int
    created_at: datetime
    items: List[OrderItem] = []
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None

class StatisticsResponse(BaseModel):
    total_sales: float
    total_orders: int
    total_products: int
    total_members: int
    recent_orders: List[dict]
    top_products: List[dict]

# 用户管理相关schema
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    status: Optional[int] = None

# 店铺管理相关schema
class ShopCreate(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    license_key: Optional[str] = None

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    license_key: Optional[str] = None
    status: Optional[int] = None

class ShopResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    license_key: Optional[str] = None
    status: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ShopList(BaseModel):
    items: List[ShopResponse]
    total: int
    skip: int
    limit: int
    has_more: bool

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    status: int
    shop_id: int
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserList(BaseModel):
    items: List[UserResponse]
    total: int
    skip: int
    limit: int
    has_more: bool