#!/usr/bin/env python3
"""
用户管理API测试脚本
"""

import requests
import json

def test_users_api():
    """测试用户管理API"""
    base_url = "http://localhost:8000"
    
    # 1. 登录获取token
    print("🔐 测试登录...")
    login_data = {
        "username": "admin",
        "password": "password"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            print(f"✅ 登录成功，用户: {data['user']['username']}")
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return False
    
    # 2. 测试获取用户列表
    print("\n👥 测试获取用户列表...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{base_url}/api/users/",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            user_count = len(data.get("items", []))
            print(f"✅ 获取用户列表成功，共 {user_count} 个用户")
            print(f"   用户列表: {[u['username'] for u in data.get('items', [])]}")
        else:
            print(f"❌ 获取用户列表失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 获取用户列表异常: {e}")
        return False
    
    # 3. 测试获取个人信息
    print("\n👤 测试获取个人信息...")
    try:
        response = requests.get(
            f"{base_url}/api/users/me/profile",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取个人信息成功")
            print(f"   用户名: {data['username']}")
            print(f"   角色: {data['role']}")
            print(f"   店铺ID: {data['shop_id']}")
        else:
            print(f"❌ 获取个人信息失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 获取个人信息异常: {e}")
        return False
    
    print("\n🎉 所有用户管理API测试通过！")
    return True

if __name__ == "__main__":
    test_users_api()
