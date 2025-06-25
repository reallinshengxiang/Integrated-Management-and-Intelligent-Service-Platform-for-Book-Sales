from .base import db

category_records = db.Table('category_records',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
)