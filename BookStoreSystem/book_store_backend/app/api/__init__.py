from flask import Blueprint
from flask import request
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from .auth.routes import AuthLogin, AuthRegister
from .books.routes import BookList, BookDetail, SearchBooksByTitle, SearchBooksByISBN, BookListPaginated, ReviewRatingStats
from app.api.books.routes import ReviewListPaginated
from .books.create_review import CreateReview

from .users.routes import UserList, UserDetail, UserRecommendation, Deepseek,UserListPaginated, UpdateUser
from .orders.routes import OrderList, OrderDetail, CreateOrder, OrderListPaginated

from .admin.books import AdminBookList, AdminBookStock

from .users.routes import UserList, UserDetail, UserRecommendation, Deepseek, UserCount

api.add_resource(AuthLogin, '/auth/login')
api.add_resource(AuthRegister, '/auth/register')

api.add_resource(UserListPaginated, '/users/paginated')
api.add_resource(UpdateUser, '/users/update')

api.add_resource(BookList, '/books')
api.add_resource(BookDetail, '/books/<int:book_id>')
api.add_resource(SearchBooksByTitle, '/books/search/title')
api.add_resource(SearchBooksByISBN, '/books/search/isbn')
api.add_resource(BookListPaginated, '/books/paginated')
api.add_resource(OrderListPaginated, '/orders/paginated')
api.add_resource(ReviewRatingStats, '/bookreviews/<int:book_id>')
api.add_resource(ReviewListPaginated, '/bookreviewscontent/<int:book_id>')
api.add_resource(CreateReview, '/bookreviews/create')

api.add_resource(UserList, '/users')
api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(UserRecommendation, '/user/recommendation/<int:user_id>')
api.add_resource(Deepseek, '/user/deepseek/<string:user_input>')

api.add_resource(OrderList, '/orders')
api.add_resource(OrderDetail, '/orders/<int:order_id>')
api.add_resource(CreateOrder, '/orders/create')

api.add_resource(AdminBookList, '/admin/books')
api.add_resource(AdminBookStock, '/admin/books/<int:book_id>/stock')

api.add_resource(UserCount, '/users/count')