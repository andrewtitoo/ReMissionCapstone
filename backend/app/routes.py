from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import User, SymptomLog
from . import db

bp = Blueprint('api', __name__)

# ---------------------- Generate User ID ----------------------

@bp.route('/generate-user', methods=['POST'])
def generate_user():
    """
    Generate a new user with a unique user_id.
    """
    try:
        user_id = str(datetime.utcnow().timestamp()).replace('.', '')[:10]  # Generate a unique 10-digit ID
        new_user = User(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: Unable to create user"}), 500

# ---------------------- Symptom Logging and Retrieval ----------------------

@bp.route('/log-symptoms', methods=['POST'])
def log_symptoms():
    """
    Log symptoms for a user including pain level, stress level, sleep hours,
    exercise, and medication information.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    required_fields = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All symptom fields are required"}), 400

    try:
        new_log = SymptomLog(
            user_id=user_id,
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
def get_symptom_logs():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        symptom_logs = SymptomLog.query.filter_by(user_id=user_id).all()
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

# --------------------- Bot Analysis ---------------------------

@bp.route('/bot-analysis', methods=['POST'])
def bot_analysis():
    """
    Analyze user's symptom logs and provide insights based on the latest log.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        latest_log = SymptomLog.query.filter_by(user_id=user_id).order_by(SymptomLog.logged_at.desc()).first()

        if not latest_log:
            return jsonify({"error": "No symptom logs available for analysis"}), 404

        # Classify based on symptom logs
        flare = 0
        if latest_log.pain_level >= 7:
            flare = 1
        elif latest_log.pain_level >= 5 and (
                latest_log.sleep_hours < 7 or
                latest_log.took_medication == 0 or
                latest_log.stress_level > 5):
            flare = 1
        elif latest_log.pain_level >= 2 and sum([
            latest_log.sleep_hours < 7,
            latest_log.took_medication == 0,
            latest_log.exercise_done == 0,
            latest_log.stress_level > 6
        ]) >= 3:
            flare = 1

        # Generate insights
        insights = []
        if flare:
            insights.append("Your recent symptom logs indicate a potential flare-up. Please take care of yourself.")
            if latest_log.pain_level > 5:
                insights.append(f"Pain Level: {latest_log.pain_level}. High pain can be challenging.")
            if latest_log.stress_level > 6:
                insights.append(f"Stress Level: {latest_log.stress_level}. High stress affects your well-being.")
            if latest_log.sleep_hours < 7:
                insights.append(f"Sleep: {latest_log.sleep_hours} hours. Aim for 7-9 hours.")
            if not latest_log.exercise_done:
                insights.append("Exercise: Consider light activities to boost your energy.")
            if not latest_log.took_medication:
                insights.append("Medication: Ensure you're following your plan.")
        else:
            insights.append("Fantastic! You seem to be in remission. Keep up your healthy habits!")

        return jsonify({
            "classification": "flare" if flare else "remission",
            "insights": insights
        }), 200

    except Exception as e:
        return jsonify({"error": "Unable to analyze symptom logs"}), 500
