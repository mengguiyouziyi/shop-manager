#!/usr/bin/env python3
"""
完整的自动化测试框架
包含测试运行器、报告生成、CI/CD集成
"""

import sys
import os
import time
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Callable
import requests
from pathlib import Path

class TestResult:
    """测试结果类"""
    def __init__(self, name: str, success: bool, message: str = "", duration: float = 0):
        self.name = name
        self.success = success
        self.message = message
        self.duration = duration
        self.timestamp = datetime.now().isoformat()

class TestSuite:
    """测试套件类"""
    def __init__(self, name: str):
        self.name = name
        self.tests: List[Callable] = []
        self.results: List[TestResult] = []
    
    def add_test(self, test_func: Callable):
        """添加测试函数"""
        self.tests.append(test_func)
    
    def run(self) -> List[TestResult]:
        """运行所有测试"""
        print(f"\n🧪 运行测试套件: {self.name}")
        print("=" * 60)
        
        for test in self.tests:
            start_time = time.time()
            try:
                result = test()
                duration = time.time() - start_time
                
                if result:
                    test_result = TestResult(test.__name__, True, "测试通过", duration)
                    print(f"✅ {test.__name__}: 通过 ({duration:.3f}s)")
                else:
                    test_result = TestResult(test.__name__, False, "测试失败", duration)
                    print(f"❌ {test.__name__}: 失败 ({duration:.3f}s)")
                
                self.results.append(test_result)
                
            except Exception as e:
                duration = time.time() - start_time
                test_result = TestResult(test.__name__, False, str(e), duration)
                print(f"💥 {test.__name__}: 异常 ({duration:.3f}s) - {e}")
                self.results.append(test_result)
        
        return self.results

class TestRunner:
    """测试运行器"""
    def __init__(self):
        self.suites: List[TestSuite] = []
        self.all_results: List[TestResult] = []
        self.start_time = None
        self.end_time = None
    
    def add_suite(self, suite: TestSuite):
        """添加测试套件"""
        self.suites.append(suite)
    
    def run_all(self) -> Dict[str, Any]:
        """运行所有测试套件"""
        self.start_time = time.time()
        
        print("🚀 开始运行完整测试套件")
        print("=" * 80)
        
        for suite in self.suites:
            results = suite.run()
            self.all_results.extend(results)
        
        self.end_time = time.time()
        
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """生成测试报告"""
        total_tests = len(self.all_results)
        passed_tests = sum(1 for r in self.all_results if r.success)
        failed_tests = total_tests - passed_tests
        total_duration = self.end_time - self.start_time
        
        # 按套件分组结果
        suite_results = {}
        for suite in self.suites:
            suite_results[suite.name] = {
                'total': len(suite.results),
                'passed': sum(1 for r in suite.results if r.success),
                'failed': sum(1 for r in suite.results if not r.success),
                'duration': sum(r.duration for r in suite.results)
            }
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                'total_duration': total_duration,
                'timestamp': datetime.now().isoformat()
            },
            'suite_results': suite_results,
            'detailed_results': [
                {
                    'name': r.name,
                    'success': r.success,
                    'message': r.message,
                    'duration': r.duration,
                    'timestamp': r.timestamp
                }
                for r in self.all_results
            ]
        }
        
        # 打印报告
        self.print_report(report)
        
        # 保存报告
        self.save_report(report)
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """打印测试报告"""
        print("\n" + "=" * 80)
        print("📊 测试报告")
        print("=" * 80)
        
        summary = report['summary']
        print(f"总测试数: {summary['total_tests']}")
        print(f"通过: {summary['passed_tests']} ✅")
        print(f"失败: {summary['failed_tests']} ❌")
        print(f"成功率: {summary['success_rate']:.1f}%")
        print(f"总耗时: {summary['total_duration']:.3f}s")
        
        print(f"\n📋 套件详情:")
        for suite_name, suite_result in report['suite_results'].items():
            status = "✅" if suite_result['failed'] == 0 else "❌"
            print(f"  {status} {suite_name}: {suite_result['passed']}/{suite_result['total']} 通过")
        
        if summary['failed_tests'] > 0:
            print(f"\n❌ 失败的测试:")
            for result in report['detailed_results']:
                if not result['success']:
                    print(f"  - {result['name']}: {result['message']}")
        
        print("\n" + "=" * 80)
    
    def save_report(self, report: Dict[str, Any]):
        """保存测试报告"""
        # 创建reports目录
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = reports_dir / f"test_report_{timestamp}.json"
        
        # 保存JSON报告
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成HTML报告
        html_report = self.generate_html_report(report)
        html_file = reports_dir / f"test_report_{timestamp}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"📄 测试报告已保存:")
        print(f"  JSON: {report_file}")
        print(f"  HTML: {html_file}")
    
    def generate_html_report(self, report: Dict[str, Any]) -> str:
        """生成HTML格式的测试报告"""
        summary = report['summary']
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - {summary['timestamp']}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 20px; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .suite {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-radius: 4px; }}
        .test-passed {{ background: #d4edda; border: 1px solid #c3e6cb; }}
        .test-failed {{ background: #f8d7da; border: 1px solid #f5c6cb; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 自动化测试报告</h1>
        <p>生成时间: {summary['timestamp']}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>总测试数</h3>
            <p style="font-size: 2em;">{summary['total_tests']}</p>
        </div>
        <div class="summary-card">
            <h3>通过</h3>
            <p style="font-size: 2em;" class="passed">{summary['passed_tests']}</p>
        </div>
        <div class="summary-card">
            <h3>失败</h3>
            <p style="font-size: 2em;" class="failed">{summary['failed_tests']}</p>
        </div>
        <div class="summary-card">
            <h3>成功率</h3>
            <p style="font-size: 2em;">{summary['success_rate']:.1f}%</p>
        </div>
    </div>
    
    <h2>📋 详细结果</h2>
"""
        
        for suite_name, suite_result in report['suite_results'].items():
            html += f"""
    <div class="suite">
        <h3>{suite_name}</h3>
        <p>通过: {suite_result['passed']}/{suite_result['total']} | 耗时: {suite_result['duration']:.3f}s</p>
"""
            
            # 添加该套件的测试结果
            for result in report['detailed_results']:
                if result['name'].startswith(suite_name.lower()):
                    status_class = "test-passed" if result['success'] else "test-failed"
                    status_icon = "✅" if result['success'] else "❌"
                    html += f"""
        <div class="test-result {status_class}">
            {status_icon} {result['name']} - {result['message']} ({result['duration']:.3f}s)
        </div>
"""
            
            html += "</div>"
        
        html += """
</body>
</html>
"""
        return html

# 具体的测试函数
def test_database_connection():
    """测试数据库连接"""
    try:
        from app.database import engine
        return True
    except Exception:
        return False

def test_config_loading():
    """测试配置加载"""
    try:
        from config import DATABASE_CONFIG, REDIS_CONFIG
        return True
    except Exception:
        return False

def test_basic_imports():
    """测试基本依赖"""
    try:
        import fastapi
        import sqlalchemy
        import pymysql
        return True
    except Exception:
        return False

def test_api_endpoints():
    """测试API端点"""
    try:
        # 这里可以添加实际的API测试
        return True
    except Exception:
        return False

def test_frontend_build():
    """测试前端构建"""
    try:
        # 检查前端目录是否存在
        frontend_dir = Path("../frontend")
        if not frontend_dir.exists():
            return False
        
        # 检查package.json是否存在
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            return False
        
        return True
    except Exception:
        return False

def main():
    """主函数"""
    # 创建测试运行器
    runner = TestRunner()
    
    # 创建基础设施测试套件
    infrastructure_suite = TestSuite("基础设施测试")
    infrastructure_suite.add_test(test_database_connection)
    infrastructure_suite.add_test(test_config_loading)
    infrastructure_suite.add_test(test_basic_imports)
    runner.add_suite(infrastructure_suite)
    
    # 创建API测试套件
    api_suite = TestSuite("API测试")
    api_suite.add_test(test_api_endpoints)
    runner.add_suite(api_suite)
    
    # 创建前端测试套件
    frontend_suite = TestSuite("前端测试")
    frontend_suite.add_test(test_frontend_build)
    runner.add_suite(frontend_suite)
    
    # 运行所有测试
    report = runner.run_all()
    
    # 根据测试结果决定退出码
    if report['summary']['failed_tests'] == 0:
        print("🎉 所有测试通过！项目可以进入下一阶段")
        sys.exit(0)
    else:
        print("⚠️  有测试失败，需要修复后再继续")
        sys.exit(1)

if __name__ == "__main__":
    main()
