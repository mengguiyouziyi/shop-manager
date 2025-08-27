#!/usr/bin/env python3
"""
修复status模块导入问题的脚本
"""

import re

def fix_status_imports():
    """修复用户管理路由中的status模块问题"""
    file_path = "app/routes/users.py"
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有的status.HTTP_* 为对应的数字
    replacements = {
        'status.HTTP_200_OK': '200',
        'status.HTTP_201_CREATED': '201',
        'status.HTTP_400_BAD_REQUEST': '400',
        'status.HTTP_401_UNAUTHORIZED': '401',
        'status.HTTP_403_FORBIDDEN': '403',
        'status.HTTP_404_NOT_FOUND': '404',
        'status.HTTP_500_INTERNAL_SERVER_ERROR': '500',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # 移除status导入
    content = content.replace('from fastapi import status', '')
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已修复status模块导入问题")

if __name__ == "__main__":
    fix_status_imports()
