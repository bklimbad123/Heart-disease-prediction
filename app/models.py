from datetime import datetime
from enum import unique

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=False, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    reports = db.relationship('Report', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    prediction = db.Column(db.Boolean, nullable=False)  # True for heart disease, False for no heart disease
    confidence = db.Column(db.Float)  # Prediction confidence

    # Store input parameters
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)  # 1 for male, 0 for female
    cp = db.Column(db.Integer, nullable=False)  # chest pain type
    trestbps = db.Column(db.Integer, nullable=False)  # resting blood pressure
    chol = db.Column(db.Integer, nullable=False)  # serum cholesterol
    fbs = db.Column(db.Integer, nullable=False)  # fasting blood sugar
    restecg = db.Column(db.Integer, nullable=False)  # resting electrocardiographic results
    thalach = db.Column(db.Integer, nullable=False)  # maximum heart rate achieved
    exang = db.Column(db.Integer, nullable=False)  # exercise induced angina
    oldpeak = db.Column(db.Float, nullable=False)  # ST depression induced by exercise
    slope = db.Column(db.Integer, nullable=False)  # slope of the peak exercise ST segment
    ca = db.Column(db.Integer, nullable=False)  # number of major vessels colored by fluoroscopy
    thal = db.Column(db.Integer, nullable=False)  # thalassemia

    def to_dict(self):
        return {
            'id': self.id,
            # 'name':self.name,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'prediction': 'Heart Disease Risk' if self.prediction else 'No Heart Disease Risk',
            'confidence': f'{self.confidence * 100:.2f}%',
            'age': self.age,
            'gender': 'Male' if self.gender == 1 else 'Female',
            'cp': self.cp,
            'trestbps': self.trestbps,
            'chol': self.chol,
            'fbs': self.fbs,
            'restecg': self.restecg,
            'thalach': self.thalach,
            'exang': self.exang,
            'oldpeak': self.oldpeak,
            'slope': self.slope,
            'ca': self.ca,
            'thal': self.thal
        }

    def get_feature_names(self):
        return {
            'name': 'name',
            'age': 'Age',
            'gender': 'Gender',
            'cp': 'Chest Pain Type',
            'trestbps': 'Resting Blood Pressure',
            'chol': 'Serum Cholesterol',
            'fbs': 'Fasting Blood Sugar',
            'restecg': 'Resting ECG Results',
            'thalach': 'Maximum Heart Rate',
            'exang': 'Exercise Induced Angina',
            'oldpeak': 'ST Depression',
            'slope': 'ST Segment Slope',
            'ca': 'Major Vessels Count',
            'thal': 'Thalassemia'
        }

    def __repr__(self):
        return f'<Report {self.id} for User {self.user_id}>'