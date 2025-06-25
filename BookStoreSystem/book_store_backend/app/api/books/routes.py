from flask_restful import Resource, reqparse
from app.service.book_service import (
    get_all_books, get_book_by_id, create_book, update_book, delete_book
)

class BookList(Resource):
    def get(self):
        books = get_all_books()
        return [{"id": book.id, "title": book.title} for book in books]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ISBN", type=str, required=True)
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("price", type=float, required=True)
        parser.add_argument("author", type=str, required=True)
        parser.add_argument("publisher_id", type=int, required=True)
        parser.add_argument("publish_date", type=str)
        parser.add_argument("stock_quantity", type=int)
        parser.add_argument("description", type=str)
        data = parser.parse_args()
        new_book = create_book(data)
        if new_book:
            return {"id": new_book.id, "title": new_book.title}, 201
        return {"message": "Failed to create book"}, 400

class BookDetail(Resource):
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if book:
            return {
                "id": book.id,
                "title": book.title,
                "price": book.price,
                "author": book.author
            }
        return {"message": "Book not found"}, 404

    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument("ISBN", type=str)
        parser.add_argument("title", type=str)
        parser.add_argument("price", type=float)
        parser.add_argument("author", type=str)
        parser.add_argument("publisher_id", type=int)
        parser.add_argument("publish_date", type=str)
        parser.add_argument("stock_quantity", type=int)
        parser.add_argument("description", type=str)
        data = parser.parse_args()
        updated_book = update_book(book_id, data)
        if updated_book:
            return {"id": updated_book.id, "title": updated_book.title}
        return {"message": "Failed to update book"}, 400

    def delete(self, book_id):
        if delete_book(book_id):
            return {"message": "Book deleted successfully"}, 200
        return {"message": "Failed to delete book"}, 400