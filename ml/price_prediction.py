import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import os

class PricePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.crop_encoder = LabelEncoder()
        self.is_trained = False
        self._train_model()
    
    def _train_model(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'price_sample_data.csv')
        if not os.path.exists(csv_path):
            self._create_sample_data(csv_path)
        
        df = pd.read_csv(csv_path)
        df['crop_encoded'] = self.crop_encoder.fit_transform(df['crop'])
        df['month'] = np.random.randint(1, 13, size=len(df))
        df['demand_index'] = np.random.randint(30, 100, size=len(df))
        df['supply_index'] = np.random.randint(20, 90, size=len(df))
        df['price'] = (df['demand_index'] * 15 + df['supply_index'] * 10 + 
                       df['rainfall'] * 0.5 + df['temperature'] * 2 + 
                       np.random.normal(0, 50, size=len(df)))
        
        X = df[['crop_encoded', 'month', 'demand_index', 'supply_index']]
        y = df['price']
        self.model.fit(X, y)
        self.is_trained = True
    
    def _create_sample_data(self, path):
        data = {
            'soil_type': ['clay', 'sandy', 'loamy', 'clay', 'sandy', 'loamy', 'clay', 'sandy', 'loamy', 'clay',
                          'sandy', 'loamy', 'clay', 'sandy', 'loamy', 'clay', 'sandy', 'loamy', 'clay', 'sandy'],
            'ph_level': [6.5, 7.0, 6.8, 6.2, 7.5, 6.9, 6.4, 7.2, 6.7, 6.3,
                         7.1, 6.8, 6.6, 7.3, 6.9, 6.5, 7.0, 6.7, 6.4, 7.4],
            'rainfall': [1200, 800, 1000, 1100, 600, 950, 1300, 750, 1050, 1150,
                         850, 980, 1250, 700, 1020, 1180, 820, 970, 1280, 650],
            'temperature': [25, 30, 28, 24, 32, 27, 26, 31, 28, 25,
                            29, 27, 25, 33, 28, 26, 30, 27, 25, 32],
            'humidity': [80, 60, 75, 85, 55, 70, 82, 58, 72, 83,
                         62, 74, 81, 57, 73, 84, 61, 76, 86, 59],
            'crop': ['rice', 'groundnut', 'wheat', 'rice', 'millet', 'wheat', 'rice', 'groundnut', 'wheat', 'rice',
                     'groundnut', 'wheat', 'rice', 'millet', 'wheat', 'rice', 'groundnut', 'wheat', 'rice', 'millet']
        }
        df = pd.DataFrame(data)
        df.to_csv(path, index=False)
    
    def predict(self, features):
        if not self.is_trained:
            return {'price': 0.0}
        
        crop = features['crop_name']
        crop_encoded = self.crop_encoder.transform([crop])[0] if crop in self.crop_encoder.classes_ else 0
        X = np.array([[crop_encoded, features['month'], features['demand_index'], features['supply_index']]])
        price = self.model.predict(X)[0]
        return {'price': round(max(price, 0), 2)}
