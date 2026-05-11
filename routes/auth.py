from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from utils.helpers import check_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    if User.find_by_username(data.get('username')):
        return jsonify({'message': 'Username already exists'}), 409
    
    if User.find_by_email(data.get('email')):
        return jsonify({'message': 'Email already exists'}), 409
    
    user_id = User.create_user(data)
    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    user = User.find_by_username(data.get('username'))
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not check_password(data.get('password'), user.get('password')):
        return jsonify({'message': 'Invalid password'}), 401
    
    if user.get('role') == 'farmer' and not user.get('is_active'):
        return jsonify({'message': 'Account pending admin approval'}), 403
    
    access_token = create_access_token(identity=user.get('username'))
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'username': user.get('username'),
            'role': user.get('role'),
            'full_name': user.get('full_name')
        }
    }), 200
