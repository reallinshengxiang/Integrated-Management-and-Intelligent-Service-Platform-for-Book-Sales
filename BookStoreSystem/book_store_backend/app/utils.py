from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from app.models import User, UserType

import logging
 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logging.debug('++++++++++++++++++++++++++++++++')
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        logging.debug('++++++++++++++++++++++++++++++++')
        logging.debug('admin required:', user_id, user.username)
        logging.debug('user.user_type', user.user_type)
        if user and user.user_type == UserType.admin:
            return fn(*args, **kwargs)
        else:
            return jsonify({'message': 'Admin privilege required'}), 403
    
    return wrapper