from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Assuming that db has been imported and initialized in __init__.py
from . import db

# Define the User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)  # Unique username for the user
    email = db.Column(db.String(120), nullable=False, unique=True)  # Unique email for user contact and login
    password_hash = db.Column(db.String(128), nullable=False)  # Password stored as a hashed value
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the user account was created

    def __repr__(self):
        return f'<User {self.username}>'

# Define the SymptomLog model to store user-reported symptoms
class SymptomLog(db.Model):
    __tablename__ = 'symptom_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to User table

    # User-reported values
    pain_level = db.Column(db.Integer, nullable=False)  # Scale of 1-10
    stress_level = db.Column(db.Integer, nullable=False)  # Scale of 1-10
    sleep_hours = db.Column(db.Float, nullable=False)  # Number of sleep hours
    exercise_done = db.Column(db.Boolean, nullable=False)  # Yes/No for exercise
    exercise_type = db.Column(db.String(50), nullable=True)  # If exercised, type of exercise (e.g., cardio, strength)
    took_medication = db.Column(db.Boolean, nullable=False)  # Yes/No for taking medication

    # Optional notes for more context
    diet_notes = db.Column(db.String(500), nullable=True)  # Notes on diet for that day
    additional_notes = db.Column(db.String(500), nullable=True)  # Any general notes from the user

    # Timestamps
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the log was created
    timestamp = db.Column(db.Time, default=datetime.now().time)  # Time of day when entry was made

    # Relationship with User
    user = db.relationship('User', backref=db.backref('symptom_logs', lazy=True))

    def __repr__(self):
        return f'<SymptomLog {self.id} by User {self.user_id}>'

# Define the Prediction model to store model predictions
class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to User table
    prediction_result = db.Column(db.String(50), nullable=False)  # Example: "Flare-up Likely" or "Stable"
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the prediction was made
    additional_info = db.Column(db.String(500), nullable=True)  # Additional information or suggestions

    # Relationship with User
    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

    def __repr__(self):
        return f'<Prediction {self.prediction_result} for User {self.user_id} at {self.predicted_at}>'

# Define the TrendAnalysis model to store insights based on the logged data
class TrendAnalysis(db.Model):
    __tablename__ = 'trend_analysis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to User table
    analysis_summary = db.Column(db.String(1000), nullable=False)  # Summary of trend analysis based on symptom logs
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the trend analysis was generated

    # Relationship with User
    user = db.relationship('User', backref=db.backref('trend_analysis', lazy=True))

    def __repr__(self):
        return f'<TrendAnalysis for User {self.user_id} at {self.generated_at}>'
