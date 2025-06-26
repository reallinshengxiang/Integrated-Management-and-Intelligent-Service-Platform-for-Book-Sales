# run.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask.cli import AppGroup
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import click

# 导入配置和模型
from app.config import Config
from app.models import db, User, Book, Order, OrderItem, Review, Publisher, Category, UserType, OrderStatus
from app.models.base import BaseModelMixin
from app.api import api_bp

# 创建 Flask 应用
app = Flask(__name__)
# print(f"TOKEN: {Config.GITHUB_TOKEN}")
app.config.from_object(Config)
# print(app.config)

# 调试：打印数据库连接字符串
# print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
# print(f"TOKEN: {app.config['GITHUB_TOKEN']}")

# 初始化扩展
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

CORS(
    app,
    supports_credentials=True,
    origins=['http://localhost:3000', 'http://127.0.0.1:3000']  # 添加前端访问地址
)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 命令行工具组
user_cli = AppGroup('user')
app.cli.add_command(user_cli)

@user_cli.command("create-admin")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_admin(username, email, password):
    """创建管理员账户"""
    if User.query.filter_by(username=username).first():
        # print(f"错误: 用户名 '{username}' 已存在")
        return
    
    if User.query.filter_by(email=email).first():
        # print(f"错误: 邮箱 '{email}' 已存在")
        return
    
    admin = User(
        username=username,
        email=email,
        user_type=UserType.ADMIN
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    
    # print(f"管理员账户 '{username}' 创建成功!")

@app.shell_context_processor
def make_shell_context():
    """为 Flask shell 提供上下文"""
    return {
        'app': app,
        'db': db,
        'User': User,
        'Book': Book,
        'Order': Order,
        'Review': Review,
        'Publisher': Publisher,
        'Category': Category,
        'UserType': UserType,
        'OrderStatus': OrderStatus
    }

# 主入口
if __name__ == '__main__':
    app.run(debug=True)