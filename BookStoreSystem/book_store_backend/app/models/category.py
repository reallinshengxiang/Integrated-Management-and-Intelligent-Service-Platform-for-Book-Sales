from .base import db, BaseModelMixin

class Category(BaseModelMixin, db.Model):
    __tablename__ = "categories"
    
    name = db.Column(db.Text) 
    description = db.Column(db.Text)  