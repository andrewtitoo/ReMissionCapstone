from flask import Blueprint, request, jsonify
from datetime import datetime
import random
from .models import User, SymptomLog
from . import db

bp = Blueprint('api', __name__)

# ---------------------- Validate or Assign User ID ----------------------

@bp.route('/auto-assign-user', methods=['POST'])
def auto_assign_user():
    """
    Validate or create a new User ID.
    """
    try:
        user_id = request.json.get('user_id')

        if user_id:
            # Validate existing user_id
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                return jsonify({"message": "User ID validated", "user_id": user.user_id}), 200
            return jsonify({"error": "Invalid User ID provided"}), 404

        # Create new user if no valid ID provided
        user_id = str(random.randint(100000, 999999))
        while User.query.filter_by(user_id=user_id).first():
            user_id = str(random.randint(100000, 999999))

        new_user = User(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User ID assigned successfully", "user_id": new_user.user_id}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error during user ID assignment: {e}")
        return jsonify({"error": f"Database error: Unable to assign user ID ({str(e)})"}), 500


# ---------------------- Symptom Logging ----------------------

@bp.route('/log-symptoms', methods=['POST'])
def log_symptoms():
    """
    Log symptoms for a user.
    """
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required."}), 400

    required_fields = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All symptom fields are required."}), 400

    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "Invalid User ID."}), 404

        # Remove any unnecessary fields like diet_notes, additional_notes
        new_log = SymptomLog(
            user_id=user_id,
            pain_level=data['pain_level'],
            stress_level=data['stress_level'],
            sleep_hours=data['sleep_hours'],
            exercise_done=data['exercise_done'],
            exercise_type=",".join(data.get('exercise_types', [])),  # Join selected exercise types
            took_medication=data['took_medication'],
            logged_at=datetime.utcnow()
        )

        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Symptom log created successfully."}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error during symptom logging: {e}")
        return jsonify({"error": f"Database error: Unable to log symptoms ({str(e)})"}), 500


# ---------------------- Retrieve Symptom Logs ----------------------

@bp.route('/symptom-logs', methods=['GET'])
def get_symptom_logs():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required."}), 400

    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "Invalid User ID."}), 404

        symptom_logs = SymptomLog.query.filter_by(user_id=user_id).order_by(SymptomLog.logged_at.desc()).all()
        response_data = [
            {
                "logged_at": log.logged_at.strftime('%Y-%m-%d %H:%M:%S'),
                "pain_level": log.pain_level,
                "stress_level": log.stress_level,
                "sleep_hours": log.sleep_hours,
                "exercise_done": log.exercise_done,
                "exercise_type": log.exercise_type.split(',') if log.exercise_type else [],
                "took_medication": log.took_medication
            }
            for log in symptom_logs
        ]
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error retrieving symptom logs: {e}")
        return jsonify({"error": f"Database error: Unable to fetch symptom logs ({str(e)})"}), 500

# ---------------------- Bot Analysis ----------------------

@bp.route('/bot-analysis', methods=['POST'])
def bot_analysis():
    """
    Analyze user's symptom logs and provide insights based on the latest log.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "User ID is required."}), 400

        latest_log = SymptomLog.query.filter_by(user_id=user_id).order_by(SymptomLog.logged_at.desc()).first()

        if not latest_log:
            return jsonify({"error": "No symptom logs available for analysis."}), 404

        # Flare-up determination
        flare = (
                latest_log.pain_level >= 7
                or (latest_log.pain_level >= 5 and (latest_log.sleep_hours < 7 or not latest_log.took_medication or latest_log.stress_level > 5))
                or (latest_log.pain_level >= 2 and sum([
            latest_log.sleep_hours < 7,
            not latest_log.took_medication,
            not latest_log.exercise_done,
            latest_log.stress_level > 6
        ]) >= 3)
        )

        # Generate Insights
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

        return jsonify({"classification": "flare" if flare else "remission", "insights": insights}), 200

    except Exception as e:
        print(f"Error analyzing logs: {e}")
        return jsonify({"error": f"Unable to analyze symptom logs ({str(e)})"}), 500
