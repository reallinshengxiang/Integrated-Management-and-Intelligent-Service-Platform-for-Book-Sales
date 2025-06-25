from .base import db, BaseModelMixin

class Review(BaseModelMixin, db.Model):
    __tablename__ = "reviews"
    

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)