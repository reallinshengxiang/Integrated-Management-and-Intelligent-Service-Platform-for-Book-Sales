from flask_restful import Resource, reqparse
from app.service.user_service import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user, book_recommendation, deepseek_response, get_user_count,
)
from app.models.user import User, UserType
from flask import request
from flask_restful import Resource
from app.models import User, db

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
            return {'id': user.id, 'username': user.username, 'email':user.email, 'phone':user.phone, 'user_type': '管理员' if user.user_type==UserType.admin else '顾客'}
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
        # print("request for userid:", user_id)
        recommendation_ids = book_recommendation(user_id)
        return {"recommendation_list": recommendation_ids}, 200

class Deepseek(Resource):
    def get(self, user_input):
        # print("Received input:", user_input)
        response = deepseek_response(user_input)
        return {"response": response}, 200


class UserListPaginated(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=20)
        args = parser.parse_args()

        users = User.query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)
        return {
            'users': [{'id': user.id, 'username': user.username, 'email':user.email, 'phone':user.phone, 'user_type': '管理员' if user.user_type==UserType.admin else '顾客'} for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page
        }

class UpdateUser(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('id')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')

        user = User.query.get(user_id)
        if not user:
            return {'message': '用户未找到'}, 404

        if username:
            user.username = username
        if password:
            user.password = password
        if email:
            user.email = email
        if phone:
            user.phone = phone

        try:
            db.session.commit()
            return {'message': '用户信息更新成功'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'更新失败: {str(e)}'}, 500

class UserCount(Resource):
    def get(self):
        count = get_user_count()
        return count


