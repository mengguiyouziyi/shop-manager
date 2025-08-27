#!/usr/bin/env python3
"""
用户管理功能测试脚本
测试用户管理的各个功能模块
"""

import sys
import os
import requests
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "admin"
TEST_PASSWORD = "password"

class UserManagementTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """记录测试结果"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {message}")
        
    def test_login(self):
        """测试用户登录"""
        try:
            login_data = {
                "username": TEST_USERNAME,
                "password": TEST_PASSWORD
            }
            response = self.session.post(
                f"{BASE_URL}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                if self.access_token:
                    self.log_test("用户登录", "PASS", f"成功登录用户: {data['user']['username']}")
                    return True
                else:
                    self.log_test("用户登录", "FAIL", "未获取到访问令牌")
                    return False
            else:
                self.log_test("用户登录", "FAIL", f"登录失败: {response.text}")
                return False
        except Exception as e:
            self.log_test("用户登录", "FAIL", f"登录异常: {str(e)}")
            return False
    
    def test_get_users_list(self):
        """测试获取用户列表"""
        if not self.access_token:
            self.log_test("获取用户列表", "SKIP", "未获取到访问令牌")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.session.get(
                f"{BASE_URL}/api/users/",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                user_count = len(data.get("items", []))
                self.log_test("获取用户列表", "PASS", f"成功获取 {user_count} 个用户")
                return True
            else:
                self.log_test("获取用户列表", "FAIL", f"状态码: {response.status_code}, 响应: {response.text}")
                return False
        except Exception as e:
            self.log_test("获取用户列表", "FAIL", f"请求异常: {str(e)}")
            return False
    
    def test_get_my_profile(self):
        """测试获取个人信息"""
        if not self.access_token:
            self.log_test("获取个人信息", "SKIP", "未获取到访问令牌")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.session.get(
                f"{BASE_URL}/api/users/me/profile",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("获取个人信息", "PASS", f"用户: {data['username']}, 角色: {data['role']}")
                return True
            else:
                self.log_test("获取个人信息", "FAIL", f"状态码: {response.status_code}, 响应: {response.text}")
                return False
        except Exception as e:
            self.log_test("获取个人信息", "FAIL", f"请求异常: {str(e)}")
            return False
    
    def test_create_user(self):
        """测试创建用户"""
        if not self.access_token:
            self.log_test("创建用户", "SKIP", "未获取到访问令牌")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            new_user_data = {
                "username": "testuser",
                "password": "testpass123",
                "name": "测试用户",
                "email": "test@example.com",
                "phone": "13900139000",
                "role": "staff",
                "shop_id": 1
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/users/",
                json=new_user_data,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("创建用户", "PASS", f"成功创建用户: {data['username']}")
                return True
            else:
                self.log_test("创建用户", "FAIL", f"状态码: {response.status_code}, 响应: {response.text}")
                return False
        except Exception as e:
            self.log_test("创建用户", "FAIL", f"请求异常: {str(e)}")
            return False
    
    def test_update_user(self):
        """测试更新用户"""
        if not self.access_token:
            self.log_test("更新用户", "SKIP", "未获取到访问令牌")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            update_data = {
                "name": "更新后的测试用户",
                "phone": "13900139001"
            }
            
            response = self.session.put(
                f"{BASE_URL}/api/users/2",  # 假设用户ID为2
                json=update_data,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("更新用户", "PASS", f"成功更新用户: {data['name']}")
                return True
            else:
                self.log_test("更新用户", "FAIL", f"状态码: {response.status_code}, 响应: {response.text}")
                return False
        except Exception as e:
            self.log_test("更新用户", "FAIL", f"请求异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始用户管理功能测试...")
        print("=" * 50)
        
        # 基础功能测试
        self.test_login()
        
        # 用户管理功能测试
        if self.access_token:
            self.test_get_users_list()
            self.test_get_my_profile()
            self.test_create_user()
            self.test_update_user()
        
        # 输出测试总结
        print("\n" + "=" * 50)
        print("📊 测试结果总结:")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIP"])
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"跳过: {skipped_tests} ⏭️")
        
        if failed_tests == 0:
            print("\n🎉 所有测试通过！用户管理功能正常。")
        else:
            print(f"\n⚠️  有 {failed_tests} 个测试失败，需要检查。")
        
        return failed_tests == 0

def main():
    """主函数"""
    tester = UserManagementTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 用户管理功能测试完成！")
        print("\n📋 下一步建议:")
        print("1. 继续开发店铺管理模块")
        print("2. 实现商品管理系统")
        print("3. 添加订单处理功能")
        print("4. 完善权限控制系统")
    else:
        print("\n🔧 用户管理功能测试发现问题，需要先修复这些问题。")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
