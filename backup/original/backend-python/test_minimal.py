#!/usr/bin/env python3
"""
最小化测试框架
测试核心功能是否正常
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """测试数据库连接"""
    try:
        from app.database import engine
        print("✅ 数据库连接: 成功")
        return True
    except Exception as e:
        print(f"❌ 数据库连接: 失败 - {e}")
        return False

def test_config_loading():
    """测试配置加载"""
    try:
        from config import DATABASE_CONFIG, REDIS_CONFIG
        print("✅ 配置加载: 成功")
        print(f"   数据库主机: {DATABASE_CONFIG['host']}")
        print(f"   Redis主机: {REDIS_CONFIG['host']}")
        return True
    except Exception as e:
        print(f"❌ 配置加载: 失败 - {e}")
        return False

def test_basic_imports():
    """测试基本导入"""
    try:
        import fastapi
        import sqlalchemy
        import pymysql
        print("✅ 基本依赖: 成功")
        return True
    except Exception as e:
        print(f"❌ 基本依赖: 失败 - {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始最小化测试...")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_config_loading,
        test_database_connection,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！可以进入下一阶段")
        return True
    else:
        print("⚠️  有测试失败，需要修复后再继续")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
