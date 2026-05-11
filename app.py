from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from extensions import db, jwt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
CORS(app)

# Basic Routes
from routes.auth import auth_bp
from routes.farmer import farmer_bp
from routes.admin import admin_bp
from routes.marketplace import marketplace_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(farmer_bp, url_prefix='/api/farmer')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(marketplace_bp, url_prefix='/api/marketplace')

# ML Route
try:
    from routes.ml import ml_bp
    app.register_blueprint(ml_bp, url_prefix='/api/ml')
except Exception as e:
    print("ML Blueprint Error:", e)

# Weather Route
try:
    from routes.weather import weather_bp
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
except Exception as e:
    print("Weather Blueprint Error:", e)

# Chat Route
try:
    from routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
except Exception as e:
    print("Chat Blueprint Error:", e)

# Notifications Route
try:
    from routes.notifications import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
except Exception as e:
    print("Notifications Blueprint Error:", e)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/farmer/dashboard')
def farmer_dashboard():
    return render_template('farmer/dashboard.html')


@app.route('/farmer/crops')
def farmer_crops():
    return render_template('farmer/crops.html')


@app.route('/farmer/expenses')
def farmer_expenses():
    return render_template('farmer/expenses.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@app.route('/admin/farmers')
def admin_farmers():
    return render_template('admin/farmers.html')


@app.route('/admin/analytics')
def admin_analytics():
    return render_template('admin/analytics.html')


@app.route('/admin/loans')
def admin_loans():
    return render_template('admin/loans.html')


@app.route('/marketplace')
def marketplace():
    return render_template('marketplace/products.html')


@app.route('/marketplace/cart')
def marketplace_cart():
    return render_template('marketplace/cart.html')


@app.route('/marketplace/orders')
def marketplace_orders():
    return render_template('marketplace/orders.html')


@app.route('/chat')
def chat_page():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()