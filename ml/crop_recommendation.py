import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

class CropRecommender:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.soil_encoder = LabelEncoder()
        self.is_trained = False
        self._train_model()
    
    def _train_model(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'crop_sample_data.csv')
        if not os.path.exists(csv_path):
            self._create_sample_data(csv_path)
        
        df = pd.read_csv(csv_path)
        df['soil_type_encoded'] = self.soil_encoder.fit_transform(df['soil_type'])
        X = df[['soil_type_encoded', 'ph_level', 'rainfall', 'temperature', 'humidity']]
        y = df['crop']
        
        self.label_encoder.fit(y)
        y_encoded = self.label_encoder.transform(y)
        self.model.fit(X, y_encoded)
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
            return {'crop': 'Unknown', 'confidence': 0.0, 'alternatives': []}
        
        soil_encoded = self.soil_encoder.transform([features['soil_type']])[0] if features['soil_type'] in self.soil_encoder.classes_ else 0
        X = np.array([[soil_encoded, features['ph_level'], features['rainfall'], features['temperature'], features['humidity']]])
        
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        crop = self.label_encoder.inverse_transform([prediction])[0]
        confidence = float(probabilities[prediction])
        
        top_indices = np.argsort(probabilities)[-3:][::-1]
        alternatives = [self.label_encoder.inverse_transform([i])[0] for i in top_indices if i != prediction]
        
        return {
            'crop': crop,
            'confidence': round(confidence * 100, 2),
            'alternatives': alternatives[:2]
        }
