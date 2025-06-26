from flask_restful import Resource, reqparse
from flask import jsonify
from app.models.review import Review
from app.models import db

class CreateReview(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int, required=True, help='user_id is required')
        self.parser.add_argument('book_id', type=int, required=True, help='book_id is required')
        self.parser.add_argument('rating', type=int, required=True, help='rating is required')
        self.parser.add_argument('comment', type=str, required=True, help='comment is required')

    def post(self):
        args = self.parser.parse_args()
        new_review = Review(
            user_id=args['user_id'],
            book_id=args['book_id'],
            rating=args['rating'],
            comment=args['comment']
        )
        try:
            db.session.add(new_review)
            db.session.commit()
            return jsonify({'message': 'Review created successfully', 'id': new_review.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to create review', 'error': str(e)}), 500