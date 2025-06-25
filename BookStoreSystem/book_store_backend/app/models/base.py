from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

db = SQLAlchemy()

class BaseModelMixin:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()