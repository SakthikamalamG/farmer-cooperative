"""
Run this once to seed 9 sample products (3 vegetables, 3 fruits, 3 grains)
under the admin account so buyers can see them in the marketplace.

Usage:
    python seed_products.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from models.user import User
from models.product import Product

SAMPLE_PRODUCTS = [
    # Vegetables
    {'name': 'Fresh Tomatoes',   'category': 'vegetables', 'price': 25,  'quantity': 100, 'unit': 'kg',    'description': 'Farm fresh red tomatoes, no pesticides', 'location': 'Coimbatore, TN'},
    {'name': 'Green Spinach',    'category': 'vegetables', 'price': 15,  'quantity': 50,  'unit': 'kg',    'description': 'Organic spinach, freshly harvested',      'location': 'Salem, TN'},
    {'name': 'Brinjal (Eggplant)','category':'vegetables', 'price': 20,  'quantity': 80,  'unit': 'kg',    'description': 'Purple brinjal, tender and fresh',         'location': 'Madurai, TN'},
    # Fruits
    {'name': 'Alphonso Mangoes', 'category': 'fruits',     'price': 120, 'quantity': 200, 'unit': 'kg',    'description': 'Sweet Alphonso mangoes from Ratnagiri',    'location': 'Ratnagiri, MH'},
    {'name': 'Bananas (Robusta)','category': 'fruits',     'price': 30,  'quantity': 150, 'unit': 'dozen', 'description': 'Fresh Robusta bananas, ripe and sweet',    'location': 'Trichy, TN'},
    {'name': 'Guava',            'category': 'fruits',     'price': 40,  'quantity': 60,  'unit': 'kg',    'description': 'White guava, rich in Vitamin C',           'location': 'Erode, TN'},
    # Grains
    {'name': 'Basmati Rice',     'category': 'grains',     'price': 65,  'quantity': 500, 'unit': 'kg',    'description': 'Long grain basmati rice, premium quality', 'location': 'Karnal, HR'},
    {'name': 'Wheat Flour',      'category': 'grains',     'price': 35,  'quantity': 300, 'unit': 'kg',    'description': 'Whole wheat flour, freshly milled',        'location': 'Ludhiana, PB'},
    {'name': 'Maize (Corn)',     'category': 'grains',     'price': 22,  'quantity': 400, 'unit': 'kg',    'description': 'Yellow maize, good for feed and flour',    'location': 'Davangere, KA'},
]

def seed():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user not found. Run python create_admin.py first.")
            return

        added = 0
        for p in SAMPLE_PRODUCTS:
            exists = Product.query.filter_by(name=p['name'], farmer_id=admin.id).first()
            if not exists:
                product = Product(
                    farmer_id   = admin.id,
                    farmer_name = 'Demo Farmer',
                    name        = p['name'],
                    category    = p['category'],
                    price       = p['price'],
                    quantity    = p['quantity'],
                    unit        = p['unit'],
                    description = p['description'],
                    location    = p['location'],
                    is_available= True   # pre-enabled for demo
                )
                db.session.add(product)
                added += 1

        db.session.commit()
        print(f"Done! {added} sample products added to marketplace.")
        print("Open http://localhost:5000/marketplace to see them.")

if __name__ == '__main__':
    seed()
