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
app.config.from_object(Config)

# 调试：打印数据库连接字符串
print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")

# 初始化扩展
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

CORS(
    app
)


# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 命令行工具组
user_cli = AppGroup('user')
app.cli.add_command(user_cli)

# # 初始化数据库命令
# @app.cli.command("init-db")
# def init_db():
#     """创建所有数据库表"""
#     db.create_all()
#     print("数据库表创建成功!")

# 创建管理员命令
@user_cli.command("create-admin")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_admin(username, email, password):
    """创建管理员账户"""
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
    db.session.add(admin)
    db.session.commit()
    
    print(f"管理员账户 '{username}' 创建成功!")

# # 创建测试数据命令
# @app.cli.command("create-test-data")
# def create_test_data():
#     """创建测试数据"""
#     # 创建出版社
#     publisher = Publisher(publisher_name="示例出版社")
#     db.session.add(publisher)
#     db.session.commit()
    
#     # 创建类别
#     category1 = Category(name="计算机科学")
#     category2 = Category(name="文学")
#     db.session.add_all([category1, category2])
#     db.session.commit()
    
#     # 创建书籍
#     book1 = Book(
#         ISBN="978-3-16-148410-0",
#         title="Python 编程从入门到精通",
#         price=99.99,
#         author="John Doe",
#         publisher_id=publisher.id,
#         stock_quantity=100,
#         description="一本全面介绍Python编程的入门书籍"
#     )
#     book1.categories.append(category1)
#     db.session.add(book1)
    
#     book2 = Book(
#         ISBN="978-3-16-148410-1",
#         title="数据结构与算法",
#         price=129.99,
#         author="Jane Smith",
#         publisher_id=publisher.id,
#         stock_quantity=50,
#         description="经典的数据结构与算法教材"
#     )
#     book2.categories.append(category1)
#     db.session.add(book2)
    
#     # 创建普通用户
#     user = User(
#         username="testuser",
#         email="test@example.com",
#         user_type=UserType.CUSTOMER
#     )
#     user.set_password("testpassword")
#     db.session.add(user)
#     db.session.commit()
    
#     # 创建订单
#     order = Order(
#         user_id=user.id,
#         status=OrderStatus.PAID,
#         total_amount=book1.price + book2.price,
#         shipping_address="北京市朝阳区"
#     )
    
#     order_item1 = OrderItem(
#         order_id=order.id,
#         book_id=book1.id,
#         quantity=1,
#         unit_price=book1.price
#     )
    
#     order_item2 = OrderItem(
#         order_id=order.id,
#         book_id=book2.id,
#         quantity=1,
#         unit_price=book2.price
#     )
    
#     db.session.add_all([order, order_item1, order_item2])
    
#     # 更新库存
#     book1.stock_quantity -= 1
#     book2.stock_quantity -= 1
    
#     db.session.commit()
#     print("测试数据创建成功!")

# 应用上下文处理器
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