from .base import db, BaseModelMixin
from enum import Enum

class InventoryOperation(Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"

class InventoryLog(BaseModelMixin, db.Model):
    __tablename__ = "inventory_logs"
    
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    change_quantity = db.Column(db.Integer, nullable=False)
    remaining_quantity = db.Column(db.Integer, nullable=False)
    operation_type = db.Column(db.Enum(InventoryOperation), nullable=False)
    related_order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))