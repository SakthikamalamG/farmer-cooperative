from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_name = db.Column(db.String(120), default='')
    name = db.Column(db.String(120))
    category = db.Column(db.String(80))
    price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20), default='kg')
    description = db.Column(db.String(255), default='')
    image_url = db.Column(db.String(255), default='')
    location = db.Column(db.String(120), default='')
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'farmer_id': str(self.farmer_id),
            'farmer_name': self.farmer_name, 'name': self.name,
            'category': self.category, 'price': self.price,
            'quantity': self.quantity, 'unit': self.unit,
            'description': self.description, 'image_url': self.image_url,
            'location': self.location, 'is_available': self.is_available
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            '_id': str(self.id), 'buyer_id': str(self.buyer_id),
            'product_id': str(self.product_id), 'quantity': self.quantity
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    buyer_name = db.Column(db.String(120), default='')
    total_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    order_type = db.Column(db.String(20), default='buy')  # 'buy' or 'preorder'
    shipping_address = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            '_id': str(self.id), 'buyer_id': str(self.buyer_id),
            'buyer_name': self.buyer_name, 'total_amount': self.total_amount,
            'status': self.status, 'order_type': self.order_type,
            'shipping_address': self.shipping_address,
            'created_at': str(self.created_at),
            'items': [i.to_dict() for i in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(50))
    product_name = db.Column(db.String(120))
    quantity = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    amount = db.Column(db.Float)
    item_type = db.Column(db.String(20), default='product')  # 'product' or 'preorder'

    def to_dict(self):
        return {
            'product_id': self.product_id, 'product_name': self.product_name,
            'quantity': self.quantity, 'unit_price': self.unit_price,
            'amount': self.amount, 'item_type': self.item_type
        }
