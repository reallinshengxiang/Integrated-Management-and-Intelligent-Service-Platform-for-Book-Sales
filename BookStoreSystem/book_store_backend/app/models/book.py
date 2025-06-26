from .base import db, BaseModelMixin
from sqlalchemy import DECIMAL, CheckConstraint
from .category_records import category_records

class Book(BaseModelMixin, db.Model):
    __tablename__ = "books"
    
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"), nullable=False)
    publish_date = db.Column(db.Date)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(DECIMAL(10, 2))
    description = db.Column(db.Text)
    cover_link = db.Column(db.String(255))
    rating = db.Column(DECIMAL(10, 2))
    
    publisher = db.relationship("Publisher", backref="books")
    reviews = db.relationship("Review", backref="book", lazy=True)
    order_items = db.relationship("OrderItem", backref="book", lazy=True)

    categories = db.relationship(
        "Category",
        secondary=category_records,
        lazy="subquery",
        backref=db.backref("book_records", lazy=True)
    )
    
    __table_args__ = (
        CheckConstraint('stock_quantity >= 0', name = 'ck_stock_quantity_nonegative'),
    )