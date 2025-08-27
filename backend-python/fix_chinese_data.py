#!/usr/bin/env python3
"""
修复数据库中文乱码问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def fix_chinese_data():
    """修复数据库中的中文数据"""
    engine = create_engine(DATABASE_URL, connect_args={'charset': 'utf8mb4'})
    
    with engine.connect() as conn:
        # 修复店铺数据
        conn.execute(text("""
            UPDATE shops 
            SET name = '测试店铺', 
                address = '测试地址123号'
            WHERE id = 1
        """))
        
        # 修复用户数据
        conn.execute(text("""
            UPDATE users 
            SET name = '管理员'
            WHERE username = 'admin' AND id = 1
        """))
        
        conn.commit()
        print("✅ 数据库中文数据修复完成")

if __name__ == "__main__":
    fix_chinese_data()