#!/usr/bin/env python3
"""
修复商品中文名称乱码问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def fix_product_chinese():
    """修复商品中的中文数据"""
    engine = create_engine(DATABASE_URL, connect_args={'charset': 'utf8mb4'})
    
    with engine.connect() as conn:
        # 修复商品数据
        products_data = [
            {
                'barcode': '6901028089685',
                'name': '方便面',
                'unit': '包'
            },
            {
                'barcode': '6901028089686',
                'name': '面包',
                'unit': '个'
            },
            {
                'barcode': '6901028089687',
                'name': '可乐',
                'unit': '瓶'
            },
            {
                'barcode': '6901028089688',
                'name': '洗发水',
                'unit': '瓶'
            }
        ]
        
        for product in products_data:
            conn.execute(text("""
                UPDATE products 
                SET name = :name, unit = :unit
                WHERE barcode = :barcode
            """), {
                'name': product['name'],
                'unit': product['unit'],
                'barcode': product['barcode']
            })
            print(f"✅ 修复商品: {product['name']} ({product['barcode']})")
        
        # 修复分类数据
        categories_data = [
            {'name': '食品'},
            {'name': '饮料'},
            {'name': '日用品'}
        ]
        
        for category in categories_data:
            conn.execute(text("""
                UPDATE categories 
                SET name = :name
                WHERE name LIKE '%食品%' OR name LIKE '%饮料%' OR name LIKE '%日用品%'
            """), {'name': category['name']})
            print(f"✅ 修复分类: {category['name']}")
        
        conn.commit()
        print("\n🎉 所有商品中文数据修复完成！")

if __name__ == "__main__":
    fix_product_chinese()
