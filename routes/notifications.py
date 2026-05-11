from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.notification import Notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user = get_jwt_identity()
    notifications = Notification.query.filter_by(username=current_user)\
        .order_by(Notification.created_at.desc()).limit(20).all()
    return jsonify([n.to_dict() for n in notifications]), 200

@notifications_bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_read():
    current_user = get_jwt_identity()
    Notification.query.filter_by(username=current_user, is_read=False)\
        .update({'is_read': True})
    db.session.commit()
    return jsonify({'message': 'Notifications marked as read'}), 200
