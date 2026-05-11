from flask import Blueprint, request, jsonify
import requests
from config import Config

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/current', methods=['GET'])
def current_weather():
    city = request.args.get('city', 'Chennai')
    params = {
        'q': city,
        'appid': Config.WEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(Config.WEATHER_API_URL, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return jsonify({
                'city': data.get('name'),
                'temperature': data['main'].get('temp'),
                'feels_like': data['main'].get('feels_like'),
                'humidity': data['main'].get('humidity'),
                'pressure': data['main'].get('pressure'),
                'weather': data['weather'][0].get('main'),
                'description': data['weather'][0].get('description'),
                'wind_speed': data['wind'].get('speed'),
                'icon': data['weather'][0].get('icon')
            }), 200
        return jsonify({'message': data.get('message', 'Error fetching weather')}), response.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@weather_bp.route('/forecast', methods=['GET'])
def weather_forecast():
    city = request.args.get('city', 'Chennai')
    params = {
        'q': city,
        'appid': Config.WEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(Config.FORECAST_API_URL, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200:
            forecasts = []
            for item in data.get('list', [])[:5]:
                forecasts.append({
                    'datetime': item.get('dt_txt'),
                    'temperature': item['main'].get('temp'),
                    'humidity': item['main'].get('humidity'),
                    'weather': item['weather'][0].get('main'),
                    'description': item['weather'][0].get('description'),
                    'wind_speed': item['wind'].get('speed')
                })
            return jsonify({
                'city': data['city'].get('name'),
                'forecasts': forecasts
            }), 200
        return jsonify({'message': data.get('message', 'Error fetching forecast')}), response.status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@weather_bp.route('/alerts', methods=['GET'])
def weather_alerts():
    return jsonify({
        'alerts': [
            {'type': 'heat_wave', 'severity': 'high', 'message': 'Expected heat wave in the coming days. Ensure adequate irrigation.'},
            {'type': 'rain', 'severity': 'medium', 'message': 'Moderate rainfall expected. Protect harvested crops.'}
        ]
    }), 200
