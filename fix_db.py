"""
Run this ONCE to fix the database — adds missing columns and seeds 9 sample products.
Usage:  python fix_db.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from models.user import User
from models.product import Product

SAMPLE_PRODUCTS = [
    # Vegetables
    {'name': 'Fresh Tomatoes',    'category': 'vegetables', 'price': 25,  'quantity': 100, 'unit': 'kg',    'description': 'Farm fresh red tomatoes, no pesticides', 'location': 'Coimbatore, TN'},
    {'name': 'Green Spinach',     'category': 'vegetables', 'price': 15,  'quantity': 50,  'unit': 'kg',    'description': 'Organic spinach, freshly harvested',      'location': 'Salem, TN'},
    {'name': 'Brinjal',           'category': 'vegetables', 'price': 20,  'quantity': 80,  'unit': 'kg',    'description': 'Purple brinjal, tender and fresh',         'location': 'Madurai, TN'},
    # Fruits
    {'name': 'Alphonso Mangoes',  'category': 'fruits',     'price': 120, 'quantity': 200, 'unit': 'kg',    'description': 'Sweet Alphonso mangoes',                   'location': 'Ratnagiri, MH'},
    {'name': 'Bananas',           'category': 'fruits',     'price': 30,  'quantity': 150, 'unit': 'dozen', 'description': 'Fresh Robusta bananas, ripe and sweet',    'location': 'Trichy, TN'},
    {'name': 'Guava',             'category': 'fruits',     'price': 40,  'quantity': 60,  'unit': 'kg',    'description': 'White guava, rich in Vitamin C',           'location': 'Erode, TN'},
    # Grains
    {'name': 'Basmati Rice',      'category': 'grains',     'price': 65,  'quantity': 500, 'unit': 'kg',    'description': 'Long grain basmati rice, premium quality', 'location': 'Karnal, HR'},
    {'name': 'Wheat',             'category': 'grains',     'price': 35,  'quantity': 300, 'unit': 'kg',    'description': 'Whole wheat, freshly milled',              'location': 'Ludhiana, PB'},
    {'name': 'Maize',             'category': 'grains',     'price': 22,  'quantity': 400, 'unit': 'kg',    'description': 'Yellow maize, good for feed and flour',    'location': 'Davangere, KA'},
]

def run_sql(conn, sql):
    try:
        conn.execute(db.text(sql))
        print(f"  OK: {sql[:60]}")
    except Exception as e:
        if 'Duplicate column' in str(e) or '1060' in str(e):
            print(f"  SKIP (already exists): {sql[:60]}")
        else:
            print(f"  ERROR: {e}")

def fix():
    with app.app_context():
        # 1. Create all tables that don't exist yet
        db.create_all()
        print("Tables created/verified.")

        # 2. Add missing columns safely
        with db.engine.connect() as conn:
            print("\nAdding missing columns...")
            run_sql(conn, "ALTER TABLE products ADD COLUMN location VARCHAR(120) DEFAULT ''")
            run_sql(conn, "ALTER TABLE orders ADD COLUMN order_type VARCHAR(20) DEFAULT 'buy'")
            run_sql(conn, "ALTER TABLE orders ADD COLUMN shipping_address VARCHAR(255) DEFAULT ''")
            run_sql(conn, "ALTER TABLE order_items ADD COLUMN item_type VARCHAR(20) DEFAULT 'product'")
            conn.commit()

        # 3. Seed sample products
        print("\nSeeding sample products...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin not found. Run: python create_admin.py first.")
            return

        added = 0
        for p in SAMPLE_PRODUCTS:
            exists = Product.query.filter_by(name=p['name'], farmer_id=admin.id).first()
            if not exists:
                product = Product(
                    farmer_id    = admin.id,
                    farmer_name  = 'Demo Farmer',
                    name         = p['name'],
                    category     = p['category'],
                    price        = p['price'],
                    quantity     = p['quantity'],
                    unit         = p['unit'],
                    description  = p['description'],
                    location     = p['location'],
                    is_available = True
                )
                db.session.add(product)
                added += 1

        db.session.commit()
        print(f"\nDone! {added} products added.")
        print("Open http://localhost:5000/marketplace — products are now visible!")

if __name__ == '__main__':
    fix()
