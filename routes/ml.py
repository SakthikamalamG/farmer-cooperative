from flask import Blueprint, request, jsonify
from ml.crop_recommendation import CropRecommender
from ml.price_prediction import PricePredictor

ml_bp = Blueprint('ml', __name__)
crop_recommender = CropRecommender()
price_predictor = PricePredictor()

@ml_bp.route('/recommend-crop', methods=['POST'])
def recommend_crop():
    data = request.get_json()
    features = {
        'soil_type': data.get('soil_type'),
        'ph_level': float(data.get('ph_level', 7.0)),
        'rainfall': float(data.get('rainfall', 0)),
        'temperature': float(data.get('temperature', 0)),
        'humidity': float(data.get('humidity', 0))
    }
    recommendation = crop_recommender.predict(features)
    return jsonify({
        'recommended_crop': recommendation['crop'],
        'confidence': recommendation['confidence'],
        'alternatives': recommendation.get('alternatives', [])
    }), 200

@ml_bp.route('/predict-price', methods=['POST'])
def predict_price():
    data = request.get_json()
    features = {
        'crop_name': data.get('crop_name'),
        'month': int(data.get('month', 1)),
        'demand_index': float(data.get('demand_index', 50)),
        'supply_index': float(data.get('supply_index', 50))
    }
    prediction = price_predictor.predict(features)
    return jsonify({
        'predicted_price': prediction['price'],
        'currency': 'INR',
        'unit': 'per_quintal'
    }), 200
