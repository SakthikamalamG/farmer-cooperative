from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.user import User

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
            if not user or user.role != required_role:
                return jsonify({'message': 'Access denied: insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    return role_required('admin')(fn)

def farmer_required(fn):
    return role_required('farmer')(fn)

def buyer_required(fn):
    return role_required('buyer')(fn)
