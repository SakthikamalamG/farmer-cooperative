import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'farmer-cooperative-secret-key-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
       "mysql+pymysql://root:lotus8%2A3@localhost:3306/farmer_cooperative"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-for-farmers')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your_openweather_api_key')
    WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
    FORECAST_API_URL = 'https://api.openweathermap.org/data/2.5/forecast'
