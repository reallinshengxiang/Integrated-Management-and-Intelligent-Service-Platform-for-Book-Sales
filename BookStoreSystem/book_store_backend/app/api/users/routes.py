from flask_restful import Resource, reqparse
from app.service.user_service import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user, book_recommendation, deepseek_response,
)

class UserList(Resource):
    def get(self):
        users = get_all_users()
        return [{"id": user.id, "username": user.username} for user in users]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("user_type", type=str, default="customer")
        data = parser.parse_args()
        new_user = create_user(data)
        if new_user:
            return {"id": new_user.id, "username": new_user.username}, 201
        return {"message": "Failed to create user"}, 400

class UserDetail(Resource):
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if user:
            return {"id": user.id, "username": user.username}
        return {"message": "User not found"}, 404

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        parser.add_argument("user_type", type=str)
        data = parser.parse_args()
        updated_user = update_user(user_id, data)
        if updated_user:
            return {"id": updated_user.id, "username": updated_user.username}
        return {"message": "Failed to update user"}, 400

    def delete(self, user_id):
        if delete_user(user_id):
            return {"message": "User deleted successfully"}, 200
        return {"message": "Failed to delete user"}, 400

class UserRecommendation(Resource):
    def get(self, user_id):
        #return {"id": 101, "recommendation_list": ["test1", "test2"]}, 200
        print("request for userid:", user_id)
        recommendation_ids = book_recommendation(user_id)
        return {"id": user_id, "recommendation_list": recommendation_ids}, 200

class Deepseek(Resource):
    def get(self, user_input):
        print("Received input:", user_input)
        response = deepseek_response(user_input)
        return {"response": response}, 200

