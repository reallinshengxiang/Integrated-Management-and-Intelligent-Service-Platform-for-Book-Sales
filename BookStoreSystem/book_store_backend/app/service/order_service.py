# book_store_backend/app/service/order_service.py
from app.models import Order, OrderItem, Book, db
from sqlalchemy.exc import IntegrityError

def get_all_orders():
    return Order.query.all()

def get_order_by_id(order_id):
    return Order.query.get(order_id)

def create_order(data):
    user_id = data.get('user_id')
    shipping_address = data.get('shipping_address')
    payment_method = data.get('payment_method')
    order_items_data = data.get('order_items', [])

    total_amount = 0
    order_items = []

    for item_data in order_items_data:
        book_id = item_data.get('book_id')
        quantity = item_data.get('quantity')
        book = Book.query.get(book_id)
        if book and book.stock_quantity >= quantity:
            total_amount += book.price * quantity
            order_item = OrderItem(
                book_id=book_id,
                quantity=quantity,
                unit_price=book.price
            )
            order_items.append(order_item)
            book.stock_quantity -= quantity
        else:
            return None

    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        shipping_address=shipping_address,
        payment_method=payment_method,
        items=order_items
    )

    try:
        db.session.add(new_order)
        db.session.commit()
        return new_order
    except IntegrityError:
        db.session.rollback()
        return None

def update_order(order_id, data):
    order = Order.query.get(order_id)
    if order:
        order.user_id = data.get('user_id', order.user_id)
        order.shipping_address = data.get('shipping_address', order.shipping_address)
        order.payment_method = data.get('payment_method', order.payment_method)
        order.status = data.get('status', order.status)

        # 更新订单项
        order_items_data = data.get('order_items', [])
        total_amount = 0
        for item_data in order_items_data:
            order_item_id = item_data.get('order_item_id')
            order_item = next((item for item in order.items if item.id == order_item_id), None)
            if order_item:
                book_id = item_data.get('book_id', order_item.book_id)
                quantity = item_data.get('quantity', order_item.quantity)
                book = Book.query.get(book_id)
                if book and book.stock_quantity + order_item.quantity >= quantity:
                    book.stock_quantity += order_item.quantity - quantity
                    order_item.book_id = book_id
                    order_item.quantity = quantity
                    order_item.unit_price = book.price
                    total_amount += book.price * quantity
                else:
                    return None
        order.total_amount = total_amount

        db.session.commit()
        return order
    return None

def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        for item in order.items:
            book = Book.query.get(item.book_id)
            book.stock_quantity += item.quantity
        db.session.delete(order)
        db.session.commit()
        return True
    return False