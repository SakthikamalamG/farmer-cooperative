# Farmer Cooperative and Management System

A full-stack web application for farmer cooperatives with AI-powered crop recommendations, price predictions, digital marketplace, weather alerts, and loan management.

## Tech Stack

- **Backend:** Python Flask (REST API)
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Database:** MongoDB
- **AI/ML:** Python (Pandas, Scikit-learn)
- **Charts:** Chart.js

## Features

### Core Features
- **User Authentication:** Role-based access (Farmer, Admin, Buyer)
- **Farmer Dashboard:** Add/manage crops, track expenses and income, view weather
- **Admin Dashboard:** Approve farmers, view analytics, manage schemes and loans
- **Marketplace:** Farmers list products, buyers browse, add to cart, and order

### Advanced Features
- **AI Crop Recommendation:** Based on soil nutrients, weather, and season
- **Price Prediction:** ML model for crop price forecasting
- **Weather Alerts:** Real-time weather updates with alert notifications
- **Chat System:** Direct messaging between farmers and buyers
- **Multi-language Support:** English and Tamil

## Project Structure

```
farmer_cooperative/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── models/                     # Database models
│   ├── user.py                 # User model (roles, auth)
│   ├── crop.py                 # Crop management model
│   ├── product.py              # Marketplace product model
│   ├── order.py                # Order model
│   └── loan.py                 # Loan/Scheme model
│
├── routes/                     # API route handlers
│   ├── auth.py                 # Authentication routes
│   ├── farmer.py               # Farmer dashboard routes
│   ├── admin.py                # Admin management routes
│   ├── marketplace.py          # Marketplace routes
│   ├── ml.py                   # ML model API routes
│   ├── weather.py              # Weather API routes
│   ├── chat.py                 # Chat messaging routes
│   └── notifications.py        # Notification routes
│
├── services/                   # Business logic services
│   ├── weather_service.py      # OpenWeatherMap API integration
│   ├── notification_service.py # In-app notifications
│   └── ml_service.py           # ML model wrapper
│
├── ml/                         # Machine Learning components
│   ├── crop_recommendation.py  # RandomForest crop recommender
│   ├── price_prediction.py     # Linear Regression price predictor
│   └── sample_data.csv         # Training dataset
│
├── utils/                      # Utilities
│   ├── decorators.py           # Role-based access control
│   └── helpers.py              # Common utilities
│
├── static/                     # Static assets
│   ├── css/style.css           # Custom styles
│   └── js/
│       ├── main.js             # Common JavaScript
│       ├── i18n.js             # English/Tamil translations
│       └── charts.js           # Chart.js configurations
│
└── templates/                  # HTML templates
    ├── base.html               # Base layout
    ├── index.html              # Landing page
    ├── login.html              # Login page
    ├── register.html           # Registration page
    ├── farmer/                 # Farmer pages
    │   ├── dashboard.html
    │   ├── crops.html
    │   └── expenses.html
    ├── admin/                  # Admin pages
    │   ├── dashboard.html
    │   ├── farmers.html
    │   ├── analytics.html
    │   └── loans.html
    ├── marketplace/            # Marketplace pages
    │   ├── products.html
    │   ├── cart.html
    │   └── orders.html
    └── chat.html               # Chat page
```

## Database Collections

| Collection | Description |
|------------|-------------|
| `users` | User accounts with roles (farmer/admin/buyer) |
| `crops` | Farmer crop records with expenses and income |
| `products` | Marketplace product listings |
| `orders` | Buyer orders with items and status |
| `loans` | Loan applications and schemes |
| `messages` | Chat messages between users |
| `notifications` | In-app user notifications |
| `schemes` | Government scheme definitions |

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/profile` | Get user profile |
| PUT | `/api/auth/profile` | Update profile |

### Farmer
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/farmer/crops` | List/Add crops |
| GET/PUT/DELETE | `/api/farmer/crops/<id>` | Crop details |
| POST | `/api/farmer/crops/<id>/expense` | Add expense |
| POST | `/api/farmer/crops/<id>/income` | Add income |
| GET/POST | `/api/farmer/products` | List/Add products |
| GET/POST | `/api/farmer/loans` | List/Apply loans |
| GET | `/api/farmer/dashboard` | Dashboard stats |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/farmers/pending` | Pending farmers |
| POST | `/api/admin/farmers/approve` | Approve farmer |
| GET | `/api/admin/farmers` | All farmers |
| GET | `/api/admin/analytics` | System analytics |
| GET | `/api/admin/loans` | Loan applications |
| POST | `/api/admin/loans/approve` | Approve loan |
| POST | `/api/admin/loans/reject` | Reject loan |
| GET/POST | `/api/admin/schemes` | List/Create schemes |

### Marketplace
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/marketplace/products` | Browse products |
| POST | `/api/marketplace/orders` | Place order |
| GET | `/api/marketplace/orders` | List orders |

### ML
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ml/recommend-crop` | AI crop recommendation |
| POST | `/api/ml/predict-price` | Price prediction |
| POST | `/api/ml/train-models` | Retrain ML models |

### Weather
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/weather/current` | Current weather |
| GET | `/api/weather/forecast` | Weather forecast |
| GET | `/api/weather/alerts` | Weather alerts |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/send` | Send message |
| GET | `/api/chat/messages/<user_id>` | Get messages |
| GET | `/api/chat/conversations` | List conversations |

## Setup Instructions

### Prerequisites
- Python 3.9+
- MongoDB (local or MongoDB Atlas)
- OpenWeatherMap API key (optional, for weather features)

### 1. Clone and Navigate
```bash
cd farmer_cooperative
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://localhost:27017/farmer_cooperative
JWT_SECRET_KEY=your-jwt-secret
WEATHER_API_KEY=your-openweather-api-key
```

### 5. Start MongoDB
Ensure MongoDB is running locally on port 27017, or update `MONGO_URI` in `config.py` to point to your MongoDB instance.

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 7. Train ML Models (First Run)
Login as admin and call the train endpoint, or the models will auto-train on first prediction request.

## Default Usage Flow

1. **Register** as Admin at `/register` (select Admin role)
2. **Register** as Farmer at `/register` (select Farmer role)
3. **Admin** approves the farmer at `/admin/farmers`
4. **Farmer** logs in and manages crops at `/farmer/crops`
5. **Farmer** lists products at `/marketplace`
6. **Buyer** registers and browses products at `/marketplace`
7. **Buyer** adds to cart and places order at `/marketplace/cart`
8. **Farmer** and **Buyer** can chat at `/chat`

## ML Model Details

### Crop Recommendation
- **Algorithm:** RandomForestClassifier
- **Features:** Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall, Soil Type, Season
- **Output:** Top 3 recommended crops with confidence scores

### Price Prediction
- **Algorithm:** LinearRegression
- **Features:** Crop name, Season, Yield per acre, Rainfall, Temperature, Humidity, Region, Quality grade, Demand index, Transport cost
- **Output:** Predicted price per kg with min/max range

## Multi-Language Support

Toggle between English and Tamil using the language dropdown in the navbar. Translations are managed in `static/js/i18n.js`.

## License

This project is open source and available for educational and commercial use.

