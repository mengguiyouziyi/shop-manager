#!/usr/bin/env python3
"""
启动诊断脚本
帮助识别后端服务启动问题
"""

import sys
import os
import traceback

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试模块导入...")
    
    try:
        print("  - 测试基础模块...")
        import fastapi
        import uvicorn
        import sqlalchemy
        print("    ✅ 基础模块导入成功")
        
        print("  - 测试认证模块...")
        from app.utils.auth import create_access_token, create_refresh_token, get_password_hash
        print("    ✅ 认证模块导入成功")
        
        print("  - 测试数据库模块...")
        from app.database import engine, Base, User, Shop
        print("    ✅ 数据库模块导入成功")
        
        print("  - 测试路由模块...")
        from app.routes import auth, users
        print("    ✅ 路由模块导入成功")
        
        print("  - 测试中间件模块...")
        from app.middleware.auth import get_current_active_user, require_roles
        print("    ✅ 中间件模块导入成功")
        
        print("  - 测试schema模块...")
        from app.schemas import UserCreate, UserUpdate, UserResponse
        print("    ✅ Schema模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"    ❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_database_connection():
    """测试数据库连接"""
    print("\n🔍 测试数据库连接...")
    
    try:
        from app.database import engine
        
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1"))
            print("    ✅ 数据库连接成功")
            return True
            
    except Exception as e:
        print(f"    ❌ 数据库连接失败: {e}")
        traceback.print_exc()
        return False

def test_auth_functions():
    """测试认证功能"""
    print("\n🔍 测试认证功能...")
    
    try:
        from app.utils.auth import create_access_token, create_refresh_token, get_password_hash
        
        # 测试密码哈希
        password = "test123"
        hashed = get_password_hash(password)
        print(f"    ✅ 密码哈希功能正常: {hashed[:20]}...")
        
        # 测试令牌生成
        data = {"sub": "testuser", "shop_id": 1}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        print(f"    ✅ 令牌生成功能正常")
        print(f"      Access Token: {access_token[:30]}...")
        print(f"      Refresh Token: {refresh_token[:30]}...")
        
        return True
        
    except Exception as e:
        print(f"    ❌ 认证功能测试失败: {e}")
        traceback.print_exc()
        return False

def test_main_app():
    """测试主应用创建"""
    print("\n🔍 测试主应用创建...")
    
    try:
        from main import app
        
        print("    ✅ 主应用创建成功")
        print(f"    - 应用标题: {app.title}")
        print(f"    - 应用版本: {app.version}")
        print(f"    - 路由数量: {len(app.routes)}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ 主应用创建失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 开始启动诊断...")
    print("=" * 50)
    
    results = []
    
    # 测试导入
    results.append(test_imports())
    
    # 测试数据库连接
    results.append(test_database_connection())
    
    # 测试认证功能
    results.append(test_auth_functions())
    
    # 测试主应用
    results.append(test_main_app())
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📊 诊断结果:")
    
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    
    print(f"总测试数: {total_tests}")
    print(f"通过: {passed_tests} ✅")
    print(f"失败: {failed_tests} ❌")
    
    if failed_tests == 0:
        print("\n🎉 所有测试通过！可以启动服务。")
        print("\n📋 建议:")
        print("1. 运行: python main.py")
        print("2. 测试API端点")
        print("3. 继续开发下一个模块")
    else:
        print(f"\n⚠️  有 {failed_tests} 个测试失败，需要先修复这些问题。")
        print("\n🔧 修复建议:")
        print("1. 检查错误日志")
        print("2. 修复导入问题")
        print("3. 检查配置文件")
        print("4. 重新运行诊断")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    exit(main())
