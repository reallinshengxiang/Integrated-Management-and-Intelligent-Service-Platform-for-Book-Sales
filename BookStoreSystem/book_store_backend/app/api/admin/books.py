from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    @jwt_required()
    @admin_required
    def patch(self, book_id):
        """修改书籍库存（管理员权限）"""
        parser = reqparse.RequestParser()
        parser.add_argument('stock', type=int, required=True)
        args = parser.parse_args()
        
        book = Book.query.get_or_404(book_id)
        book.stock_quantity = args['stock']
        book.save()
        
        return {'message': 'Stock updated', 'stock': book.stock_quantity}