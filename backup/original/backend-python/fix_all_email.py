#!/usr/bin/env python3
"""
全面修复email字段引用的脚本
"""

def fix_all_email_references():
    """修复用户管理路由中的所有email字段引用"""
    file_path = "app/routes/users.py"
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有的email相关引用
    replacements = [
        # 移除email字段检查
        ('if user_data.email:', 'if False:'),
        ('if user_data.email is not None:', 'if False:'),
        
        # 移除email字段赋值
        ('email=user_data.email,', ''),
        ('user.email = user_data.email', '# user.email = user_data.email'),
        ('current_user.email = user_data.email', '# current_user.email = user_data.email'),
        
        # 移除email字段查询
        ('existing_email = db.query(User).filter(', 'existing_email = None'),
        ('User.email == user_data.email,', 'False,'),
        ('User.email == user_data.email', 'False'),
        
        # 移除email字段条件
        ('if existing_email:', 'if False:'),
        ('if user_data.email != user.email:', 'if False:'),
        ('if user_data.email != current_user.email:', 'if False:'),
        
        # 移除email字段更新
        ('user.email = user_data.email', '# user.email = user_data.email'),
        ('current_user.email = user_data.email', '# current_user.email = user_data.email'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 已全面修复email字段引用问题")

if __name__ == "__main__":
    fix_all_email_references()
