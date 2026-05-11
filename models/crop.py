from extensions import db
from datetime import datetime

class Crop(db.Model):
    __tablename__ = 'crops'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_name = db.Column(db.String(100))
    variety = db.Column(db.String(100), default='')
    area = db.Column(db.Float)
    soil_type = db.Column(db.String(50), default='')
    season = db.Column(db.String(50), default='')
    yield_estimate = db.Column(db.String(50), default='')
    planting_date = db.Column(db.String(50))
    expected_harvest = db.Column(db.String(50))
    status = db.Column(db.String(20), default='growing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'farmer_id': str(self.farmer_id),
            'crop_name': self.crop_name, 'variety': self.variety,
            'area': self.area, 'soil_type': self.soil_type,
            'season': self.season, 'yield_estimate': self.yield_estimate,
            'planting_date': self.planting_date, 'expected_harvest': self.expected_harvest,
            'status': self.status
        }

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(100))
    amount = db.Column(db.Float, default=0)
    description = db.Column(db.String(255))
    date = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'farmer_id': str(self.farmer_id),
            'type': self.type, 'amount': self.amount,
            'description': self.description, 'date': self.date
        }

class Income(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    source = db.Column(db.String(100))
    amount = db.Column(db.Float, default=0)
    description = db.Column(db.String(255))
    date = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'farmer_id': str(self.farmer_id),
            'source': self.source, 'amount': self.amount,
            'description': self.description, 'date': self.date
        }
