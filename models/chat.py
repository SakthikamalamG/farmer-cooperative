from extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50))
    sender_name = db.Column(db.String(120), default='')
    receiver_id = db.Column(db.String(50))
    content = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'sender_id': self.sender_id,
            'sender_name': self.sender_name, 'receiver_id': self.receiver_id,
            'content': self.content, 'is_read': self.is_read,
            'created_at': str(self.created_at)
        }
