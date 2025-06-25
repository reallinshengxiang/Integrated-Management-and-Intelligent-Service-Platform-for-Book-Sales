from .base import db, BaseModelMixin

class Publisher(BaseModelMixin, db.Model):
    __tablename__ = "publishers"
    
    publisher_name = db.Column(db.String(200))