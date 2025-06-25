from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from .auth.routes import AuthLogin, AuthRegister
from .books.routes import BookList, BookDetail

from .users.routes import UserList, UserDetail, UserRecommendation, Deepseek
from .orders.routes import OrderList, OrderDetail

from .admin.books import AdminBookList, AdminBookStock

api.add_resource(AuthLogin, '/auth/login')
api.add_resource(AuthRegister, '/auth/register')
api.add_resource(BookList, '/books')
api.add_resource(BookDetail, '/books/<int:book_id>')

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(UserRecommendation, '/user/recommendation/<int:user_id>')
api.add_resource(Deepseek, '/user/deepseek/<string:user_input>')

api.add_resource(OrderList, '/orders')
api.add_resource(OrderDetail, '/orders/<int:order_id>')

api.add_resource(AdminBookList, '/admin/books')
api.add_resource(AdminBookStock, '/admin/books/<int:book_id>/stock')