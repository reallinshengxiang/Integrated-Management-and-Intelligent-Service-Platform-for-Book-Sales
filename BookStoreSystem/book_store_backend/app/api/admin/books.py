from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.models import Book, User
from app.utils import admin_required

class AdminBookList(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        """获取所有书籍（管理员权限）"""
        books = Book.query.all()
        return [{'id': b.id, 'title': b.title, 'stock': b.stock_quantity} for b in books]

class AdminBookStock(Resource):
    def post(self, book_id):
        """修改书籍库存（管理员权限）"""
        print(request.args)
        print('--------------')
        print(book_id)
        parser = reqparse.RequestParser()
        print('--------------')
        parser.add_argument('stock_quantity', type=int, required=True)
        print('--------------')
        try:
            args = parser.parse_args()
        except Exception as err:
            print(err)
        args['stock'] = 1
        print('--------------')
        book = Book.query.get_or_404(book_id)
        book.stock_quantity = args['stock']
        print('--------------')
        print(args['stock'])
        book.save()
        
        return {'message': 'Stock updated', 'stock': book.stock_quantity}