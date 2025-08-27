#!/usr/bin/env python3
"""
创建测试用户数据
用于开发和测试目的
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, User, Shop
from app.utils.auth import get_password_hash

def create_test_data():
    """创建测试数据"""
    db = SessionLocal()
    
    try:
        print("🚀 开始创建测试数据...")
        
        # 检查是否已存在测试数据
        existing_shop = db.query(Shop).filter(Shop.name == "测试店铺").first()
        if existing_shop:
            print("✅ 测试数据已存在，跳过创建")
            return
        
        # 创建测试店铺
        print("📦 创建测试店铺...")
        test_shop = Shop(
            name="测试店铺",
            address="测试地址",
            phone="13800138000",
            status=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(test_shop)
        db.commit()
        db.refresh(test_shop)
        print(f"✅ 测试店铺创建成功: {test_shop.name} (ID: {test_shop.id})")
        
        # 创建测试用户
        print("👤 创建测试用户...")
        
        # 管理员用户
        admin_user = User(
            username="admin",
            password=get_password_hash("password"),
            name="管理员",
            phone="13800138001",
            role="admin",
            shop_id=test_shop.id,
            status=1,
            created_at=datetime.utcnow()
        )
        db.add(admin_user)
        
        # 普通用户
        normal_user = User(
            username="user",
            password=get_password_hash("password"),
            name="普通用户",
            phone="13800138002",
            role="user",
            shop_id=test_shop.id,
            status=1,
            created_at=datetime.utcnow()
        )
        db.add(normal_user)
        
        db.commit()
        print("✅ 测试用户创建成功:")
        print(f"   - 管理员: admin / password")
        print(f"   - 普通用户: user / password")
        print(f"   - 店铺ID: {test_shop.id}")
        
        print("\n🎉 测试数据创建完成！")
        print("现在可以使用以下账户登录:")
        print(f"用户名: admin, 密码: password, 店铺ID: {test_shop.id}")
        print(f"用户名: user, 密码: password, 店铺ID: {test_shop.id}")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
