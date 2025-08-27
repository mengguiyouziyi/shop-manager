#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
测试远程MySQL和Redis连接是否正常
"""

import sys
import os
import time
from datetime import datetime

# 添加父目录到路径，以便导入config模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DATABASE_URL, REDIS_URL

def test_mysql_connection():
    """测试MySQL连接"""
    print("🔍 测试MySQL连接...")
    print(f"数据库URL: {DATABASE_URL}")
    
    try:
        # 尝试导入SQLAlchemy
        from sqlalchemy import create_engine, text
        
        # 创建引擎
        print("正在创建数据库引擎...")
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
        
        # 测试连接
        print("正在测试数据库连接...")
        with engine.connect() as conn:
            # 执行简单查询
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ MySQL连接成功！测试查询结果: {row[0]}")
            
            # 测试数据库版本
            result = conn.execute(text("SELECT VERSION() as version"))
            row = result.fetchone()
            print(f"📊 MySQL版本: {row[0]}")
            
            # 测试数据库列表
            result = conn.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result.fetchall()]
            print(f"🗄️ 可用数据库: {', '.join(databases)}")
            
            # 检查目标数据库是否存在
            target_db = DATABASE_URL.split('/')[-1].split('?')[0]
            if target_db in databases:
                print(f"✅ 目标数据库 '{target_db}' 存在")
                
                # 切换到目标数据库
                conn.execute(text(f"USE {target_db}"))
                
                # 检查表结构
                result = conn.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
                if tables:
                    print(f"📋 数据库中的表: {', '.join(tables)}")
                else:
                    print("📋 数据库中没有表")
            else:
                print(f"⚠️ 目标数据库 '{target_db}' 不存在")
                
        return True
        
    except ImportError as e:
        print(f"❌ 导入SQLAlchemy失败: {e}")
        print("请确保已安装: pip install sqlalchemy pymysql")
        return False
        
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        print(f"错误类型: {type(e).__name__}")
        return False

def test_redis_connection():
    """测试Redis连接"""
    print("\n🔍 测试Redis连接...")
    print(f"Redis URL: {REDIS_URL}")
    
    try:
        # 尝试导入redis
        import redis
        
        # 解析Redis配置
        from urllib.parse import urlparse
        parsed = urlparse(REDIS_URL)
        
        # 创建Redis客户端
        r = redis.Redis(
            host=parsed.hostname,
            port=parsed.port or 6379,
            db=int(parsed.path[1:]) if parsed.path else 0,
            decode_responses=True
        )
        
        # 测试连接
        print("正在测试Redis连接...")
        r.ping()
        print("✅ Redis连接成功！")
        
        # 测试基本操作
        test_key = "test_connection"
        test_value = f"test_{datetime.now().isoformat()}"
        
        r.set(test_key, test_value)
        retrieved_value = r.get(test_key)
        
        if retrieved_value == test_value:
            print("✅ Redis读写测试成功！")
        else:
            print(f"⚠️ Redis读写测试失败: 期望 {test_value}, 实际 {retrieved_value}")
        
        # 清理测试数据
        r.delete(test_key)
        
        # 获取Redis信息
        info = r.info()
        print(f"📊 Redis版本: {info.get('redis_version', '未知')}")
        print(f"📊 已用内存: {info.get('used_memory_human', '未知')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入redis失败: {e}")
        print("请确保已安装: pip install redis")
        return False
        
    except Exception as e:
        print(f"❌ Redis连接失败: {e}")
        print(f"错误类型: {type(e).__name__}")
        return False

def test_network_connectivity():
    """测试网络连通性"""
    print("\n🔍 测试网络连通性...")
    
    import socket
    
    # 测试MySQL端口
    mysql_host = "192.168.1.246"
    mysql_port = 3306
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((mysql_host, mysql_port))
        sock.close()
        
        if result == 0:
            print(f"✅ MySQL端口 {mysql_port} 可达")
        else:
            print(f"❌ MySQL端口 {mysql_port} 不可达")
            return False
    except Exception as e:
        print(f"❌ 网络测试失败: {e}")
        return False
    
    # 测试Redis端口
    redis_port = 6379
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((mysql_host, redis_port))
        sock.close()
        
        if result == 0:
            print(f"✅ Redis端口 {redis_port} 可达")
        else:
            print(f"❌ Redis端口 {redis_port} 不可达")
            return False
    except Exception as e:
        print(f"❌ 网络测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始数据库连接测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 测试网络连通性
    network_ok = test_network_connectivity()
    
    if not network_ok:
        print("\n❌ 网络连通性测试失败，无法继续数据库测试")
        return
    
    # 测试MySQL连接
    mysql_ok = test_mysql_connection()
    
    # 测试Redis连接
    redis_ok = test_redis_connection()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 测试结果总结")
    print("=" * 50)
    print(f"网络连通性: {'✅ 正常' if network_ok else '❌ 失败'}")
    print(f"MySQL连接: {'✅ 正常' if mysql_ok else '❌ 失败'}")
    print(f"Redis连接: {'✅ 正常' if redis_ok else '❌ 失败'}")
    
    if mysql_ok and redis_ok:
        print("\n🎉 所有数据库连接测试通过！")
        print("✅ 可以继续开发后端服务")
    else:
        print("\n⚠️ 部分数据库连接测试失败")
        print("请检查网络配置和数据库服务状态")

if __name__ == "__main__":
    main()
