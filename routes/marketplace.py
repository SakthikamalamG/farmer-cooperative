from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.product import Product, Cart, Order, OrderItem
from models.crop import Crop

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        data = request.get_json()
        product = Product(
            farmer_id=user.id,
            farmer_name=user.full_name,
            name=data.get('name'),
            category=data.get('category'),
            price=float(data.get('price', 0)),
            quantity=float(data.get('quantity', 0)),
            unit=data.get('unit', 'kg'),
            description=data.get('description', ''),
            image_url=data.get('image_url', '')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product listed', 'product_id': str(product.id)}), 201

    products_list = Product.query.filter_by(is_available=True).all()
    return jsonify([p.to_dict() for p in products_list]), 200

@marketplace_bp.route('/crops', methods=['GET'])
def marketplace_crops():
    crops = Crop.query.filter_by(status='growing').all()
    result = []
    for c in crops:
        farmer = User.query.get(c.farmer_id)
        result.append({
            '_id': str(c.id),
            'crop_name': c.crop_name,
            'variety': c.variety or '',
            'area': c.area,
            'season': c.season or '',
            'yield_estimate': c.yield_estimate or '',
            'soil_type': c.soil_type or '',
            'planting_date': c.planting_date or '',
            'expected_harvest': c.expected_harvest or '',
            'status': c.status,
            'farmer_name': farmer.full_name if farmer else 'Unknown',
            'farmer_id': str(c.farmer_id)
        })
    return jsonify(result), 200

@marketplace_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200

@marketplace_bp.route('/cart', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def cart():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        product_id = int(data.get('product_id'))
        item = Cart.query.filter_by(buyer_id=user.id, product_id=product_id).first()
        if item:
            item.quantity = float(data.get('quantity', 1))
        else:
            item = Cart(buyer_id=user.id, product_id=product_id, quantity=float(data.get('quantity', 1)))
            db.session.add(item)
        db.session.commit()
        return jsonify({'message': 'Added to cart'}), 200

    if request.method == 'DELETE':
        data = request.get_json()
        Cart.query.filter_by(buyer_id=user.id, product_id=int(data.get('product_id'))).delete()
        db.session.commit()
        return jsonify({'message': 'Removed from cart'}), 200

    cart_items = Cart.query.filter_by(buyer_id=user.id).all()
    result = []
    for item in cart_items:
        d = item.to_dict()
        product = Product.query.get(item.product_id)
        if product:
            d['product_name'] = product.name
            d['price'] = product.price
            d['unit'] = product.unit
        result.append(d)
    return jsonify(result), 200

@marketplace_bp.route('/orders', methods=['GET', 'POST'])
@jwt_required()
def orders():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if request.method == 'POST':
        data = request.get_json()
        items = data.get('items', [])
        if not items:
            return jsonify({'message': 'Cart is empty'}), 400
        total_amount  = float(data.get('total_amount', 0))
        order_type    = data.get('order_type', 'buy')
        shipping_addr = data.get('shipping_address', '')
        order = Order(
            buyer_id=user.id, buyer_name=user.full_name or user.username,
            total_amount=total_amount, order_type=order_type,
            shipping_address=shipping_addr
        )
        db.session.add(order)
        db.session.flush()
        for item in items:
            oi = OrderItem(
                order_id=order.id,
                product_id=str(item.get('product_id', '')),
                product_name=item.get('name', ''),
                quantity=float(item.get('quantity', 1)),
                unit_price=float(item.get('price', 0)),
                amount=float(item.get('quantity', 1)) * float(item.get('price', 0)),
                item_type=item.get('item_type', 'product')
            )
            db.session.add(oi)
        db.session.commit()
        return jsonify({'message': 'Order placed', 'order_id': str(order.id)}), 201

    if user.role == 'buyer':
        orders_list = Order.query.filter_by(buyer_id=user.id).order_by(Order.created_at.desc()).all()
    else:
        orders_list = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders_list]), 200
