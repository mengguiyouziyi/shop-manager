#!/usr/bin/env python3
"""
初始化数据库脚本
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, Shop, User, Category, Product, Member
from app.utils.auth import get_password_hash

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_database():
    """初始化数据库"""
    print("正在连接数据库...")
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建表
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    
    # 创建示例数据
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        shop_count = db.query(Shop).count()
        if shop_count > 0:
            print("数据库中已有数据，跳过初始化")
            return
        
        print("创建示例数据...")
        
        # 创建店铺
        shop = Shop(
            name="测试店铺",
            address="测试地址123号",
            phone="13800138000",
            license_key="DEMO-001"
        )
        db.add(shop)
        db.commit()
        db.refresh(shop)
        
        # 创建用户
        admin_user = User(
            shop_id=shop.id,
            username="admin",
            password=get_password_hash("password"),
            role="admin",
            name="管理员",
            phone="13800138000"
        )
        
        staff_user = User(
            shop_id=shop.id,
            username="staff",
            password=get_password_hash("password"),
            role="staff",
            name="员工",
            phone="13800138001"
        )
        
        db.add(admin_user)
        db.add(staff_user)
        
        # 创建分类
        categories = [
            Category(shop_id=shop.id, name="食品"),
            Category(shop_id=shop.id, name="饮料"),
            Category(shop_id=shop.id, name="日用品")
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # 刷新分类以获取ID
        db.refresh(categories[0])
        db.refresh(categories[1])
        db.refresh(categories[2])
        
        # 创建商品
        products = [
            Product(
                shop_id=shop.id,
                category_id=categories[0].id,
                name="方便面",
                barcode="6901028089685",
                price=5.50,
                cost_price=4.00,
                stock=100,
                unit="包"
            ),
            Product(
                shop_id=shop.id,
                category_id=categories[0].id,
                name="面包",
                barcode="6901028089686",
                price=8.00,
                cost_price=6.00,
                stock=50,
                unit="个"
            ),
            Product(
                shop_id=shop.id,
                category_id=categories[1].id,
                name="可乐",
                barcode="6901028089687",
                price=3.00,
                cost_price=2.00,
                stock=200,
                unit="瓶"
            ),
            Product(
                shop_id=shop.id,
                category_id=categories[2].id,
                name="洗发水",
                barcode="6901028089688",
                price=25.00,
                cost_price=20.00,
                stock=30,
                unit="瓶"
            )
        ]
        
        for product in products:
            db.add(product)
        
        # 创建会员
        members = [
            Member(
                shop_id=shop.id,
                name="张三",
                phone="13900139000",
                points=100,
                balance=50.00
            ),
            Member(
                shop_id=shop.id,
                name="李四",
                phone="13900139001",
                points=200,
                balance=100.00
            )
        ]
        
        for member in members:
            db.add(member)
        
        db.commit()
        
        print("数据库初始化完成！")
        print(f"店铺ID: {shop.id}")
        print(f"管理员用户: admin / password")
        print(f"员工用户: staff / password")
        
    except Exception as e:
        print(f"初始化数据库时发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()