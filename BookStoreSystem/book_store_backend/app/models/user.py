from .base import db, BaseModelMixin
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class UserType(Enum):
    customer = "customer"
    admin = "admin"
    
class User(BaseModelMixin, db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(50), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    user_type = db.Column(db.Enum(UserType), nullable = False, default = UserType.customer)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    orders = db.relationship("Order", backref="user", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        return create_access_token(identity=self.id)
    