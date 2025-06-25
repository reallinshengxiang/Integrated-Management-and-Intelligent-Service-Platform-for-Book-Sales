from flask import Flask
from werkzeug.security import generate_password_hash
from .models import User, UserType

def register_commands(app: Flask):
    """注册命令行命令"""
    
    @app.cli.command("create-admin")
    def create_admin():
        """创建管理员账户"""
        username = input("请输入管理员用户名: ")
        email = input("请输入管理员邮箱: ")
        password = input("请输入管理员密码: ")
        
        if User.query.filter_by(username=username).first():
            print(f"错误: 用户名 '{username}' 已存在")
            return
        
        if User.query.filter_by(email=email).first():
            print(f"错误: 邮箱 '{email}' 已存在")
            return
        
        admin = User(
            username=username,
            email=email,
            user_type=UserType.ADMIN
        )
        admin.set_password(password)
        admin.save()
        
        print(f"管理员账户 '{username}' 创建成功!")