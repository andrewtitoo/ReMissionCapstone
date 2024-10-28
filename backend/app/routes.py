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

# Endpoint to register a new user
@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user by storing the username, email, and hashed password.
    """
    data = request.get_json()

    # Extract and validate user data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields (username, email, password) are required"}), 400

    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists"}), 400

    # Hash the password and create a new user
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=password_hash)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while registering"}), 500

# Endpoint to log in a user
@bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user by validating credentials and returning a JWT token.
    """
    data = request.get_json()

    # Extract and validate user data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    # Verify password
    if user and bcrypt.check_password_hash(user.password_hash, password):
        # Create a JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ---------------------- Symptom Logging and Retrieval ----------------------

# Endpoint to log user symptoms
@bp.route('/log-symptoms', methods=['POST'])
@jwt_required()
def log_symptoms():
    """
    Log symptoms for a user including pain level, stress level, sleep hours,
    exercise, and medication information. Each input should align with the structured
    sliding bars and checkboxes on the frontend.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Extract and validate user-reported data
    pain_level = data.get('pain_level')
    stress_level = data.get('stress_level')
    sleep_hours = data.get('sleep_hours')
    exercise_done = data.get('exercise_done')
    exercise_type = data.get('exercise_type', None)
    took_medication = data.get('took_medication')

    # Validate data
    if pain_level is None or stress_level is None or sleep_hours is None or exercise_done is None or took_medication is None:
        return jsonify({"error": "All symptom fields are required"}), 400

    if exercise_done and not exercise_type:
        return jsonify({"error": "Exercise type is required if exercise was done"}), 400

    # Create a new symptom log entry
    new_log = SymptomLog(
        user_id=current_user_id,
        pain_level=pain_level,
        stress_level=stress_level,
        sleep_hours=sleep_hours,
        exercise_done=exercise_done,
        exercise_type=exercise_type,
        took_medication=took_medication,
        logged_at=datetime.utcnow()
    )

    try:
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Symptom log created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while logging symptoms"}), 500

# Endpoint to retrieve symptom logs
@bp.route('/symptom-logs', methods=['GET'])
@jwt_required()
def get_symptom_logs():
    """
    Retrieve all logged symptoms for the current user.
    """
    current_user_id = get_jwt_identity()

    # Query all symptom logs for the current user
    symptom_logs = SymptomLog.query.filter_by(user_id=current_user_id).all()

    # Format the data for response
    response_data = [
        {
            "id": log.id,
            "pain_level": log.pain_level,
            "stress_level": log.stress_level,
            "sleep_hours": log.sleep_hours,
            "exercise_done": log.exercise_done,
            "exercise_type": log.exercise_type,
            "took_medication": log.took_medication,
            "logged_at": log.logged_at,
        } for log in symptom_logs
    ]

    return jsonify(response_data), 200

# ---------------------- Prediction Endpoint ----------------------

# Endpoint to get a prediction on flare-up likelihood
@bp.route('/predict-flare', methods=['POST'])
@jwt_required()
def predict_flare():
    """
    Use the logged symptoms to make a prediction about potential flare-ups.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Extract relevant fields
    pain_level = data.get('pain_level')
    stress_level = data.get('stress_level')
    sleep_hours = data.get('sleep_hours')
    exercise_done = data.get('exercise_done')
    took_medication = data.get('took_medication')

    # Here we would use the predictor model (currently a placeholder) to generate a prediction.
    # For now, we'll return a mock prediction.
    prediction_result = "Flare-up Likely" if stress_level > 7 or pain_level > 8 else "Stable"
    additional_info = "High stress levels and high pain levels may indicate a potential flare-up. Consider taking steps to lower stress."

    new_prediction = Prediction(
        user_id=current_user_id,
        prediction_result=prediction_result,
        additional_info=additional_info,
        predicted_at=datetime.utcnow()
    )

    try:
        db.session.add(new_prediction)
        db.session.commit()
        return jsonify({
            "prediction_result": prediction_result,
            "additional_info": additional_info
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while generating the prediction"}), 500
