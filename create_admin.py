"""
Run this script once to create the admin user.
Usage: python create_admin.py
Default credentials: username=admin, password=admin123
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from models.user import User
from utils.helpers import hash_password

def create_admin(username='admin', password='admin123', email='admin@farmercooperative.com'):
    with app.app_context():
        import models
        db.create_all()
        if User.query.filter_by(username=username).first():
            print(f"Admin user '{username}' already exists.")
            return
        admin = User(
            username=username,
            email=email,
            password=hash_password(password),
            role='admin',
            full_name='System Administrator',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created successfully!")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Login at: http://localhost:5000/login")

if __name__ == '__main__':
    create_admin()
