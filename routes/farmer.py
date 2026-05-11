from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.crop import Crop, Expense, Income
from models.product import Product
from utils.decorators import farmer_required
from datetime import datetime

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route('/crops', methods=['GET', 'POST'])
@jwt_required()
@farmer_required
def crops():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        crop = Crop(
            farmer_id=user.id,
            crop_name=data.get('crop_name'),
            variety=data.get('variety', ''),
            area=data.get('area'),
            soil_type=data.get('soil_type', ''),
            season=data.get('season', ''),
            yield_estimate=data.get('yield_estimate', ''),
            planting_date=data.get('planting_date'),
            expected_harvest=data.get('expected_harvest')
        )
        db.session.add(crop)
        db.session.commit()
        return jsonify({'message': 'Crop added', 'crop_id': str(crop.id)}), 201

    crops_list = Crop.query.filter_by(farmer_id=user.id).all()
    return jsonify([c.to_dict() for c in crops_list]), 200

@farmer_bp.route('/products', methods=['GET', 'POST'])
@jwt_required()
@farmer_required
def farmer_products():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if request.method == 'POST':
        data = request.get_json()
        product = Product(
            farmer_id=user.id,
            farmer_name=user.full_name or user.username,
            name=data.get('name'),
            category=data.get('category', ''),
            price=float(data.get('price', 0)),
            quantity=float(data.get('quantity', 0)),
            unit=data.get('unit', 'kg'),
            description=data.get('description', ''),
            image_url=data.get('image_url', ''),
            location=data.get('location', user.location or ''),
            is_available=False
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product listed', 'product_id': str(product.id)}), 201
    products_list = Product.query.filter_by(farmer_id=user.id).all()
    return jsonify([p.to_dict() for p in products_list]), 200

@farmer_bp.route('/products/<int:product_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@farmer_required
def farmer_product_detail(product_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    product = Product.query.filter_by(id=product_id, farmer_id=user.id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    if request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200
    data = request.get_json()
    product.name        = data.get('name', product.name)
    product.category    = data.get('category', product.category)
    product.price       = float(data.get('price', product.price))
    product.quantity    = float(data.get('quantity', product.quantity))
    product.unit        = data.get('unit', product.unit)
    product.description = data.get('description', product.description)
    product.location    = data.get('location', product.location)
    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

@farmer_bp.route('/crops/<int:crop_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@farmer_required
def crop_detail(crop_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    crop = Crop.query.filter_by(id=crop_id, farmer_id=user.id).first()
    if not crop:
        return jsonify({'message': 'Crop not found'}), 404
    if request.method == 'DELETE':
        db.session.delete(crop)
        db.session.commit()
        return jsonify({'message': 'Crop deleted'}), 200
    data = request.get_json()
    crop.crop_name       = data.get('crop_name', crop.crop_name)
    crop.variety         = data.get('variety', crop.variety)
    crop.area            = data.get('area', crop.area)
    crop.soil_type       = data.get('soil_type', crop.soil_type)
    crop.season          = data.get('season', crop.season)
    crop.yield_estimate  = data.get('yield_estimate', crop.yield_estimate)
    crop.planting_date   = data.get('planting_date', crop.planting_date)
    crop.expected_harvest= data.get('expected_harvest', crop.expected_harvest)
    crop.status          = data.get('status', crop.status)
    db.session.commit()
    return jsonify({'message': 'Crop updated'}), 200

@farmer_bp.route('/products/<int:product_id>/toggle', methods=['POST'])
@jwt_required()
def toggle_product(product_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    # allow farmer (own product) or admin
    if user.role == 'farmer':
        product = Product.query.filter_by(id=product_id, farmer_id=user.id).first()
    else:
        product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    product.is_available = not product.is_available
    db.session.commit()
    return jsonify({'message': 'Updated', 'is_available': product.is_available}), 200

@farmer_bp.route('/expenses', methods=['GET', 'POST'])
@jwt_required()
@farmer_required
def expenses():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        expense = Expense(
            farmer_id=user.id,
            type=data.get('type'),
            amount=float(data.get('amount', 0)),
            description=data.get('description'),
            date=data.get('date')
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify({'message': 'Expense recorded', 'expense_id': str(expense.id)}), 201

    expenses_list = Expense.query.filter_by(farmer_id=user.id).all()
    return jsonify([e.to_dict() for e in expenses_list]), 200

@farmer_bp.route('/income', methods=['GET', 'POST'])
@jwt_required()
@farmer_required
def income():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        inc = Income(
            farmer_id=user.id,
            source=data.get('source'),
            amount=float(data.get('amount', 0)),
            description=data.get('description'),
            date=data.get('date')
        )
        db.session.add(inc)
        db.session.commit()
        return jsonify({'message': 'Income recorded', 'income_id': str(inc.id)}), 201

    incomes_list = Income.query.filter_by(farmer_id=user.id).all()
    return jsonify([i.to_dict() for i in incomes_list]), 200

@farmer_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@farmer_required
def dashboard():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    crops_list = Crop.query.filter_by(farmer_id=user.id).all()
    products_list = Product.query.filter_by(farmer_id=user.id, is_available=True).all()
    total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(farmer_id=user.id).scalar() or 0
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(farmer_id=user.id).scalar() or 0

    return jsonify({
        'total_crops': len(crops_list),
        'total_products': len(products_list),
        'total_expenses': total_expenses,
        'total_income': total_income,
        'net_profit': total_income - total_expenses,
        'crops': [{'name': c.crop_name, 'status': c.status, 'yield_estimate': c.yield_estimate} for c in crops_list],
        'products': [{'name': p.name, 'price_per_kg': p.price, 'quantity_kg': p.quantity} for p in products_list]
    }), 200
