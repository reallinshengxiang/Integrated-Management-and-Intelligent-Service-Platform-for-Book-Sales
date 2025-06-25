from .base import db, BaseModelMixin
from sqlalchemy import DECIMAL, func, CheckConstraint
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(BaseModelMixin, db.Model):
    __tablename__ = "orders"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_date = db.Column(db.TIMESTAMP, server_default = func.now())
    total_amount = db.Column(DECIMAL(10, 2), nullable=False, default=0)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING) 
    shipping_address = db.Column(db.Text)
    payment_method = db.Column(db.String(50)) 
    
    items = db.relationship("OrderItem", backref="order", lazy=True)
    
    __table_args__ = (
        CheckConstraint('total_amount > 0', name = 'ck_order_total_amount_positive'),
    )