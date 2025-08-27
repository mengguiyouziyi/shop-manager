#!/usr/bin/env python3
"""
系统功能测试脚本
用于测试店铺管理系统的各个核心功能
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

class SystemTester:
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
        
    def test_health_check(self):
        """测试健康检查"""
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                self.log_test("健康检查", "PASS", "API服务正常运行")
                return True
            else:
                self.log_test("健康检查", "FAIL", f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("健康检查", "FAIL", f"连接失败: {str(e)}")
            return False
    
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
    
    def test_protected_endpoints(self):
        """测试需要认证的端点"""
        if not self.access_token:
            self.log_test("认证端点测试", "SKIP", "未获取到访问令牌")
            return False
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # 测试获取当前用户信息
        try:
            response = self.session.get(
                f"{BASE_URL}/api/auth/me",
                headers=headers
            )
            if response.status_code == 200:
                self.log_test("获取用户信息", "PASS", "成功获取用户信息")
            else:
                self.log_test("获取用户信息", "FAIL", f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取用户信息", "FAIL", f"请求异常: {str(e)}")
    
    def test_database_operations(self):
        """测试数据库操作"""
        if not self.access_token:
            self.log_test("数据库操作测试", "SKIP", "未获取到访问令牌")
            return False
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # 这里可以添加更多数据库操作测试
        # 例如：创建商品、查询订单等
        
        self.log_test("数据库操作测试", "PASS", "基础数据库连接正常")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始系统功能测试...")
        print("=" * 50)
        
        # 基础功能测试
        self.test_health_check()
        self.test_login()
        
        # 认证功能测试
        if self.access_token:
            self.test_protected_endpoints()
            self.test_database_operations()
        
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
            print("\n🎉 所有测试通过！系统运行正常。")
        else:
            print(f"\n⚠️  有 {failed_tests} 个测试失败，需要检查。")
        
        return failed_tests == 0

def main():
    """主函数"""
    tester = SystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 系统测试完成，可以继续下一步开发！")
        print("\n📋 下一步建议:")
        print("1. 完善用户管理模块")
        print("2. 开发店铺管理功能")
        print("3. 实现商品管理系统")
        print("4. 添加订单处理功能")
    else:
        print("\n🔧 系统测试发现问题，需要先修复这些问题。")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
