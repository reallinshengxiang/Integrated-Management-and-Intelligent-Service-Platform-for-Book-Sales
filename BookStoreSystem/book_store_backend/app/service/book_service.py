# book_store_backend/app/service/book_service.py
from app.models import Book, db

def get_all_books():
    return Book.query.all()

def get_book_by_id(book_id):
    return Book.query.get(book_id)

def create_book(data):
    new_book = Book(
        ISBN=data.get('ISBN'),
        title=data.get('title'),
        price=data.get('price'),
        author=data.get('author'),
        publisher_id=data.get('publisher_id'),
        publish_date=data.get('publish_date'),
        stock_quantity=data.get('stock_quantity', 0),
        description=data.get('description'),
        cover_link=data.get('cover_link'),
        rating=data.get('rating'),
    )
    db.session.add(new_book)
    db.session.commit()
    return new_book

def update_book(book_id, data):
    book = Book.query.get(book_id)
    if book:
        book.ISBN = data.get('ISBN', book.ISBN)
        book.title = data.get('title', book.title)
        book.price = data.get('price', book.price)
        book.author = data.get('author', book.author)
        book.publisher_id = data.get('publisher_id', book.publisher_id)
        book.publish_date = data.get('publish_date', book.publish_date)
        book.stock_quantity = data.get('stock_quantity', book.stock_quantity)
        book.description = data.get('description', book.description)
        book.cover_link = data.get('cover_link', book.cover_link)
        book.rating = data.get('rating', book.rating)
        db.session.commit()
        return book
    return None

def search_books_by_title(title_substring):
    return Book.query.filter(Book.title.contains(title_substring)).all()


def search_books_by_isbn(isbn_substring):
    return Book.query.filter(Book.isbn.contains(isbn_substring)).all()


def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return True
    return False