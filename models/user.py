from extensions import db
from utils.helpers import hash_password
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='farmer')
    full_name = db.Column(db.String(120), default='')
    phone = db.Column(db.String(20), default='')
    location = db.Column(db.String(120), default='')
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id),
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'full_name': self.full_name,
            'phone': self.phone,
            'location': self.location,
            'is_active': self.is_active,
            'created_at': self.created_at
        }

    @staticmethod
    def create_user(data):
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=hash_password(data.get('password')),
            role=data.get('role', 'farmer'),
            full_name=data.get('full_name', ''),
            phone=data.get('phone', ''),
            location=data.get('location', ''),
            is_active=False if data.get('role') == 'farmer' else True
        )
        db.session.add(user)
        db.session.commit()
        return str(user.id)

    @staticmethod
    def find_by_username(username):
        user = User.query.filter_by(username=username).first()
        return user.to_dict() if user else None

    @staticmethod
    def find_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user.to_dict() if user else None

    @staticmethod
    def find_by_id(user_id):
        user = User.query.get(int(user_id))
        return user.to_dict() if user else None

    @staticmethod
    def get_pending_farmers():
        users = User.query.filter_by(role='farmer', is_active=False).all()
        return [u.to_dict() for u in users]

    @staticmethod
    def get_all_farmers():
        users = User.query.filter_by(role='farmer').all()
        return [u.to_dict() for u in users]

    @staticmethod
    def approve_farmer(user_id):
        user = User.query.get(int(user_id))
        if user:
            user.is_active = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_user(user_id, update_data):
        user = User.query.get(int(user_id))
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            db.session.commit()
            return True
        return False
