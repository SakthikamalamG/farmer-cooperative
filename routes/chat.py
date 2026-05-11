from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.chat import Message
from sqlalchemy import or_, and_

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    me = User.query.filter_by(username=current_user).first()
    users = User.query.filter(User.id != me.id, User.is_active == True).all()
    return jsonify([{'_id': str(u.id), 'full_name': u.full_name or u.username, 'role': u.role} for u in users]), 200

@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    current_user = get_jwt_identity()
    sender = User.query.filter_by(username=current_user).first()
    data = request.get_json()
    msg = Message(
        sender_id=str(sender.id),
        sender_name=sender.full_name or sender.username,
        receiver_id=str(data.get('receiver_id')),
        content=data.get('message') or data.get('content', '')
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({'message': 'Message sent', 'message_id': str(msg.id)}), 201

@chat_bp.route('/messages/<other_user_id>', methods=['GET'])
@jwt_required()
def get_conversation(other_user_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    uid = str(user.id)
    oid = str(other_user_id)
    msgs = Message.query.filter(
        or_(
            and_(Message.sender_id == uid, Message.receiver_id == oid),
            and_(Message.sender_id == oid, Message.receiver_id == uid)
        )
    ).order_by(Message.created_at.asc()).all()
    Message.query.filter(
        Message.sender_id == oid, Message.receiver_id == uid, Message.is_read == False
    ).update({'is_read': True})
    db.session.commit()
    return jsonify([m.to_dict() for m in msgs]), 200

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    uid = str(user.id)
    msgs = Message.query.filter(
        or_(Message.sender_id == uid, Message.receiver_id == uid)
    ).order_by(Message.created_at.desc()).all()
    seen = {}
    for m in msgs:
        other = m.receiver_id if m.sender_id == uid else m.sender_id
        if other not in seen:
            seen[other] = m
    result = []
    for other_id, last_msg in seen.items():
        other_user = User.query.get(int(other_id))
        unread = Message.query.filter_by(sender_id=other_id, receiver_id=uid, is_read=False).count()
        result.append({
            'user_id': other_id,
            'user_name': other_user.full_name or other_user.username if other_user else 'Unknown',
            'last_message': last_msg.content,
            'unread_count': unread
        })
    return jsonify(result), 200

@chat_bp.route('/mark-read/<other_user_id>', methods=['POST'])
@jwt_required()
def mark_read(other_user_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    Message.query.filter_by(
        sender_id=str(other_user_id), receiver_id=str(user.id), is_read=False
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'message': 'Marked read'}), 200
