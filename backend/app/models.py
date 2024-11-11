from datetime import datetime
from . import db

# Simplified User model for unique user_id generation
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), unique=True, nullable=False)  # Unique 5-6 digit user ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for user creation

    def __repr__(self):
        return f'<User {self.user_id}>'

# Updated SymptomLog model to use user_id as foreign key
class SymptomLog(db.Model):
    __tablename__ = 'symptom_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), db.ForeignKey('users.user_id'), nullable=False)

    pain_level = db.Column(db.Integer, nullable=False)
    stress_level = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    exercise_done = db.Column(db.Boolean, nullable=False)
    exercise_type = db.Column(db.String(50), nullable=True)
    took_medication = db.Column(db.Boolean, nullable=False)

    diet_notes = db.Column(db.String(500), nullable=True)
    additional_notes = db.Column(db.String(500), nullable=True)

    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp = db.Column(db.Time, default=datetime.now().time)

    user = db.relationship('User', backref=db.backref('symptom_logs', lazy=True))

    def __repr__(self):
        return f'<SymptomLog {self.id} by User {self.user_id}>'

class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), db.ForeignKey('users.user_id'), nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)
    additional_info = db.Column(db.String(500), nullable=True)

    user = db.relationship('User', backref=db.backref('predictions', lazy=True))

    def __repr__(self):
        return f'<Prediction {self.prediction_result} for User {self.user_id} at {self.predicted_at}>'

class TrendAnalysis(db.Model):
    __tablename__ = 'trend_analysis'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), db.ForeignKey('users.user_id'), nullable=False)
    analysis_summary = db.Column(db.String(1000), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('trend_analysis', lazy=True))

    def __repr__(self):
        return f'<TrendAnalysis for User {self.user_id} at {self.generated_at}>'
