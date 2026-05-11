from extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'username': self.username,
            'message': self.message, 'is_read': self.is_read,
            'created_at': str(self.created_at)
        }
