#!/usr/bin/env python3
"""
修复updated_at字段引用的脚本
"""

def fix_updated_at_references():
    """修复用户管理路由中的updated_at字段引用"""
    file_path = "app/routes/users.py"
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有的updated_at相关引用
    replacements = [
        # 移除updated_at字段赋值
        ('user.updated_at = datetime.utcnow()', '# user.updated_at = datetime.utcnow()'),
        ('current_user.updated_at = datetime.utcnow()', '# current_user.updated_at = datetime.utcnow()'),
        ('updated_at=datetime.utcnow()', '# updated_at=datetime.utcnow()'),
        
        # 移除updated_at字段访问
        ('"updated_at": user.updated_at.isoformat() if user.updated_at else None', '"updated_at": None'),
        ('"updated_at": new_user.updated_at.isoformat() if new_user.updated_at else None', '"updated_at": None'),
        ('"updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None', '"updated_at": None'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已修复updated_at字段引用问题")

if __name__ == "__main__":
    fix_updated_at_references()
