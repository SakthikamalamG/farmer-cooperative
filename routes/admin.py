from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.user import User
from models.crop import Crop
from models.product import Product, Order
from models.loan import LoanApplication, Scheme
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/farmers/pending', methods=['GET'])
@jwt_required()
@admin_required
def pending_farmers():
    farmers = User.query.filter_by(role='farmer', is_active=False).all()
    result = [f.to_dict() for f in farmers]
    for f in result:
        f.pop('password', None)
    return jsonify(result), 200

@admin_bp.route('/farmers/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_farmer():
    data = request.get_json()
    farmer_id = data.get('farmer_id')
    if not farmer_id:
        return jsonify({'message': 'farmer_id required'}), 400
    success = User.approve_farmer(farmer_id)
    if success:
        return jsonify({'message': 'Farmer approved successfully'}), 200
    return jsonify({'message': 'Farmer not found'}), 404

@admin_bp.route('/farmers', methods=['GET'])
@jwt_required()
@admin_required
def all_farmers():
    farmers = User.query.filter_by(role='farmer').all()
    result = [f.to_dict() for f in farmers]
    for f in result:
        f.pop('password', None)
    return jsonify(result), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def all_users():
    users = User.query.all()
    result = [u.to_dict() for u in users]
    for u in result:
        u.pop('password', None)
    return jsonify(result), 200

@admin_bp.route('/products', methods=['GET'])
@jwt_required()
@admin_required
def all_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@admin_bp.route('/crops', methods=['GET'])
@jwt_required()
@admin_required
def all_crops():
    crops = Crop.query.all()
    result = []
    for c in crops:
        d = c.to_dict()
        farmer = User.query.get(c.farmer_id)
        d['farmer_name'] = (farmer.full_name or farmer.username) if farmer else 'Unknown'
        result.append(d)
    return jsonify(result), 200

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
@admin_required
def analytics():
    total_farmers  = User.query.filter_by(role='farmer').count()
    total_buyers   = User.query.filter_by(role='buyer').count()
    total_crops    = Crop.query.count()
    total_orders   = Order.query.count()
    total_products = Product.query.count()
    order_revenue  = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0

    crop_production = {}
    for crop in Crop.query.all():
        ct = crop.crop_name or 'Unknown'
        crop_production[ct] = crop_production.get(ct, 0) + 1

    orders_by_status = {}
    for order in Order.query.all():
        s = order.status or 'pending'
        orders_by_status[s] = orders_by_status.get(s, 0) + 1

    return jsonify({
        'total_farmers': total_farmers, 'total_buyers': total_buyers,
        'total_crops': total_crops, 'total_orders': total_orders,
        'total_products': total_products, 'order_revenue': order_revenue,
        'crop_production': crop_production, 'orders_by_status': orders_by_status
    }), 200

@admin_bp.route('/loans', methods=['GET'])
@jwt_required()
@admin_required
def loans():
    return jsonify([a.to_dict() for a in LoanApplication.query.all()]), 200

@admin_bp.route('/loans/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_loan():
    data = request.get_json()
    loan = LoanApplication.query.get(int(data.get('loan_id')))
    if loan:
        loan.status = 'approved'
        db.session.commit()
    return jsonify({'message': 'Loan approved'}), 200

@admin_bp.route('/loans/reject', methods=['POST'])
@jwt_required()
@admin_required
def reject_loan():
    data = request.get_json()
    loan = LoanApplication.query.get(int(data.get('loan_id')))
    if loan:
        loan.status = 'rejected'
        db.session.commit()
    return jsonify({'message': 'Loan rejected'}), 200

@admin_bp.route('/schemes', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def schemes():
    if request.method == 'POST':
        data = request.get_json()
        scheme = Scheme(
            name=data.get('name'),
            description=data.get('description'),
            eligibility=data.get('eligibility'),
            benefits=str(data.get('benefits', []))
        )
        db.session.add(scheme)
        db.session.commit()
        return jsonify({'message': 'Scheme created', 'scheme_id': str(scheme.id)}), 201
    return jsonify([s.to_dict() for s in Scheme.query.all()]), 200

@admin_bp.route('/loans/apply', methods=['POST'])
@jwt_required()
def apply_loan():
    data = request.get_json()
    application = LoanApplication(
        farmer_id=data.get('farmer_id'),
        scheme_name=data.get('scheme_name', ''),
        loan_amount=float(data.get('loan_amount', 0)),
        interest_rate=float(data.get('interest_rate', 0))
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': 'Loan application submitted', 'application_id': str(application.id)}), 201
