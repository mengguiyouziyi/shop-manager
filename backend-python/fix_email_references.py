#!/usr/bin/env python3
"""
修复email字段引用的脚本
"""

def fix_email_references():
    """修复用户管理路由中的email字段引用"""
    file_path = "app/routes/users.py"
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有的email相关引用
    replacements = [
        ('"email": user.email,', ''),
        ('"email": new_user.email,', ''),
        ('"email": current_user.email,', ''),
        ('existing_email = db.query(User).filter(User.email == user_data.email).first()', 'existing_email = None'),
        ('if user_data.email != user.email:', 'if False:'),
        ('User.email == user_data.email,', 'False,'),
        ('user.email = user_data.email', '# user.email = user_data.email'),
        ('if user_data.email != current_user.email:', 'if False:'),
        ('User.email == user_data.email,', 'False,'),
        ('current_user.email = user_data.email', '# current_user.email = user_data.email'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已修复email字段引用问题")

if __name__ == "__main__":
    fix_email_references()
