from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import sys
import os

# 添加父目录到路径，以便导入config模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300, connect_args={'charset': 'utf8mb4'})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    license_key = Column(String(50), unique=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    users = relationship("User", back_populates="shop")
    categories = relationship("Category", back_populates="shop")
    products = relationship("Product", back_populates="shop")
    members = relationship("Member", back_populates="shop")
    orders = relationship("Order", back_populates="shop")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="staff")
    name = Column(String(50))
    phone = Column(String(20))
    status = Column(Integer, default=1)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="users")
    orders = relationship("Order", back_populates="operator")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="categories")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(100), nullable=False)
    barcode = Column(String(50), unique=True)
    price = Column(Float, nullable=False)
    cost_price = Column(Float)
    stock = Column(Integer, default=0)
    unit = Column(String(20))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="products")
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    name = Column(String(50))
    phone = Column(String(20), nullable=False)
    level_id = Column(Integer, default=1)
    points = Column(Integer, default=0)
    balance = Column(Float, default=0)
    birthday = Column(DateTime)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="members")
    orders = relationship("Order", back_populates="member")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    order_no = Column(String(50), unique=True, nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"))
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    payment_method = Column(String(20))
    payment_status = Column(Integer, default=0)
    status = Column(Integer, default=1)
    operator_id = Column(Integer, ForeignKey("users.id"))
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="orders")
    member = relationship("Member", back_populates="orders")
    operator = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()