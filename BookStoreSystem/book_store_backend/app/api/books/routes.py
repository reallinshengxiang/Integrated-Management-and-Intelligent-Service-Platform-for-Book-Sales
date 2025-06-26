from flask_restful import Resource, reqparse
from decimal import Decimal
import json
from app.service.book_service import (search_books_by_title, search_books_by_isbn, 
    get_all_books, get_book_by_id, create_book, update_book, delete_book
)
from app.models.book import Book
from app.models.review import Review

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

class SearchBooksByTitle(Resource):
    def post(self):
        # #print("Request Headers:", request.headers)  # 添加日志输出请求头信息
        parser = reqparse.RequestParser()
        parser.add_argument('title_substring', type=str, required=True)
        args = parser.parse_args()
        books = search_books_by_title(args['title_substring'])
        return [{'id': book.id, 'title': book.title, 'isbn': book.isbn, 'price': str(book.price)} for book in books]

class SearchBooksByISBN(Resource):
    def post(self):
        # #print("Request Headers:", request.headers)  # 添加日志输出请求头信息
        parser = reqparse.RequestParser()
        parser.add_argument('isbn_substring', type=str, required=True)
        args = parser.parse_args()
        books = search_books_by_isbn(args['isbn_substring'])
        return [{'id': book.id, 'title': book.title, 'isbn': book.isbn, 'price': str(book.price)} for book in books]

class ReviewRatingStats(Resource):
    def get(self, book_id):
        reviews = Review.query.filter_by(book_id=book_id).all()
        rating_count = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
        for review in reviews:
            rating_count[review.rating] += 1
        return rating_count

class BookDetail(Resource):
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if book:
            return {
                "id": book.id,
                "title": book.title,
                "price": str(book.price),
                "author": book.author,
                "rating": str(book.rating),
                "description": book.description,
                "publisher_id": book.publisher_id
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
    
class BookListPaginated(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        args = parser.parse_args()

        books = Book.query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)
        return {
            'books': [{'id': book.id, 'title': book.title, 'author':book.author, 'publisher_id':book.publisher_id,
                       'stock_quantity': book.stock_quantity, 'price': str(book.price), 'rating': str(book.rating)} for book in books.items],
            'total': books.total,
            'pages': books.pages,
            'current_page': books.page
        }
        
class ReviewListPaginated(Resource):
    def post(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        args = parser.parse_args()

        reviews = Review.query.filter_by(book_id=book_id).paginate(page=args['page'], per_page=args['per_page'], error_out=False)
        return {
            'reviews': [{'id': review.id, 'user_id': review.user_id, 'rating': review.rating, 'comment': review.comment} for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': reviews.page
        }
