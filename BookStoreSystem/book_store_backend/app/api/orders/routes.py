from flask_restful import Resource, reqparse
from app.service.order_service import (
    get_all_orders, get_order_by_id, create_order, update_order, delete_order
)

class OrderList(Resource):
    def get(self):
        orders = get_all_orders()
        return [{"id": order.id, "user_id": order.user_id} for order in orders]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("shipping_address", type=str, required=True)
        parser.add_argument("payment_method", type=str, required=True)
        parser.add_argument("order_items", type=list, location="json", required=True)
        data = parser.parse_args()
        new_order = create_order(data)
        if new_order:
            return {"id": new_order.id, "user_id": new_order.user_id}, 201
        return {"message": "Failed to create order"}, 400

class OrderDetail(Resource):
    def get(self, order_id):
        order = get_order_by_id(order_id)
        if order:
            return {
                "id": order.id,
                "user_id": order.user_id,
                "total_amount": order.total_amount,
                "status": order.status
            }
        return {"message": "Order not found"}, 404

    def put(self, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int)
        parser.add_argument("shipping_address", type=str)
        parser.add_argument("payment_method", type=str)
        parser.add_argument("status", type=str)
        parser.add_argument("order_items", type=list, location="json")
        data = parser.parse_args()
        updated_order = update_order(order_id, data)
        if updated_order:
            return {"id": updated_order.id, "user_id": updated_order.user_id}
        return {"message": "Failed to update order"}, 400

    def delete(self, order_id):
        if delete_order(order_id):
            return {"message": "Order deleted successfully"}, 200
        return {"message": "Failed to delete order"}, 400