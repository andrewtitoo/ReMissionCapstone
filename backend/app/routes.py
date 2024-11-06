from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from .models import User, SymptomLog, Prediction
from . import db

# Set up Blueprint, bcrypt for hashing passwords, and db (already initialized in __init__.py)
bp = Blueprint('api', __name__)
bcrypt = Bcrypt()

# ---------------------- User Registration and Authentication ----------------------

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user by storing the username, email, and hashed password.
    """
    data = request.get_json()
    required_fields = ['username', 'email', 'password']

    # Validate required fields
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields (username, email, password) are required"}), 400

    username, email, password = data['username'], data['email'], data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=password_hash)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: Unable to register user"}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user by validating credentials and returning a JWT token.
    """
    data = request.get_json()
    required_fields = ['email', 'password']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Email and password are required"}), 400

    email, password = data['email'], data['password']
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


# ---------------------- Symptom Logging and Retrieval ----------------------

@bp.route('/log-symptoms', methods=['POST'])
@jwt_required()
def log_symptoms():
    """
    Log symptoms for a user including pain level, stress level, sleep hours,
    exercise, and medication information.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "All symptom fields are required"}), 400

    if data['exercise_done'] and not data.get('exercise_type'):
        return jsonify({"error": "Exercise type is required if exercise was done"}), 400

    try:
        new_log = SymptomLog(
            user_id=current_user_id,
            pain_level=data['pain_level'],
            stress_level=data['stress_level'],
            sleep_hours=data['sleep_hours'],
            exercise_done=data['exercise_done'],
            exercise_type=data.get('exercise_type'),
            took_medication=data['took_medication'],
            logged_at=datetime.utcnow()
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Symptom log created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: Unable to log symptoms"}), 500


@bp.route('/symptom-logs', methods=['GET'])
@jwt_required()
def get_symptom_logs():
    """
    Retrieve all logged symptoms for the current user.
    """
    current_user_id = get_jwt_identity()
    try:
        symptom_logs = SymptomLog.query.filter_by(user_id=current_user_id).all()
        response_data = [
            {
                "id": log.id,
                "pain_level": log.pain_level,
                "stress_level": log.stress_level,
                "sleep_hours": log.sleep_hours,
                "exercise_done": log.exercise_done,
                "exercise_type": log.exercise_type,
                "took_medication": log.took_medication,
                "logged_at": log.logged_at
            }
            for log in symptom_logs
        ]
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": "Database error: Unable to fetch symptom logs"}), 500


# ---------------------- Prediction Endpoint ----------------------

@bp.route('/predict-flare', methods=['POST'])
@jwt_required()
def predict_flare():
    """
    Use the logged symptoms to make a prediction about potential flare-ups.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    required_fields = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "All prediction fields are required"}), 400

    try:
        # Mock prediction logic
        prediction_result = "Flare-up Likely" if data['stress_level'] > 7 or data['pain_level'] > 8 else "Stable"
        additional_info = "High stress or pain levels may indicate a potential flare-up. Take appropriate measures."

        new_prediction = Prediction(
            user_id=current_user_id,
            prediction_result=prediction_result,
            additional_info=additional_info,
            predicted_at=datetime.utcnow()
        )

        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            "prediction_result": prediction_result,
            "additional_info": additional_info
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: Unable to generate prediction"}), 500
