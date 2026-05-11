from extensions import db
from datetime import datetime

class LoanApplication(db.Model):
    __tablename__ = 'loan_applications'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.String(50))
    scheme_name = db.Column(db.String(120), default='')
    loan_amount = db.Column(db.Float, default=0)
    interest_rate = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'farmer_id': self.farmer_id,
            'scheme_name': self.scheme_name, 'loan_amount': self.loan_amount,
            'interest_rate': self.interest_rate, 'status': self.status
        }

class Scheme(db.Model):
    __tablename__ = 'schemes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    benefits = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'name': self.name,
            'description': self.description, 'eligibility': self.eligibility,
            'benefits': self.benefits
        }
