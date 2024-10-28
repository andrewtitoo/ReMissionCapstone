import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

# Import the db instance and models from the backend app module
from .. import db  # Assuming this file is within `backend/app/ml/`
from ..models import SymptomLog, TrendAnalysis

class TrendAnalyzer:
    """
    A class to analyze trends in user symptom logs to generate insights.
    This class helps CHIIP detect patterns in the user's health data
    and generate proactive suggestions.
    """

    def __init__(self, user_id, db_session: Session):
        """
        Initialize the TrendAnalyzer with a specific user.

        Args:
            user_id (int): The ID of the user to analyze.
            db_session (Session): SQLAlchemy session for database interactions.
        """
        self.user_id = user_id
        self.db_session = db_session
        self.data = None

    def load_user_data(self):
        """
        Load historical symptom logs for the user.
        """
        try:
            # Query the database for all symptom logs of the user
            symptom_logs = self.db_session.query(SymptomLog).filter_by(user_id=self.user_id).all()

            # Convert queried logs to a DataFrame for easier analysis
            self.data = pd.DataFrame([{
                "logged_at": log.logged_at,
                "pain_level": log.pain_level,
                "stress_level": log.stress_level,
                "sleep_hours": log.sleep_hours,
                "exercise_done": log.exercise_done,
                "took_medication": log.took_medication,
                "exercise_type": log.exercise_type
            } for log in symptom_logs])

            if self.data.empty:
                print(f"No data available for user {self.user_id}")
            else:
                print(f"Data successfully loaded for user {self.user_id}")

        except Exception as e:
            print(f"An error occurred while loading data for user {self.user_id}: {e}")

    def analyze_trends(self):
        """
        Analyze user data to identify trends and generate insights.

        Returns:
            str: A summary of detected trends.
        """
        if self.data is None or self.data.empty:
            return "No data available for trend analysis."

        trend_summary = []

        # Analyze pain levels and identify high-pain frequency
        high_pain_logs = self.data[self.data['pain_level'] > 7]
        if not high_pain_logs.empty:
            trend_summary.append(f"High pain levels recorded on {len(high_pain_logs)} occasions. Consider reviewing potential triggers.")

        # Stress and sleep correlation analysis
        average_stress = self.data['stress_level'].mean()
        average_sleep = self.data['sleep_hours'].mean()

        if average_stress > 6:
            trend_summary.append(f"Average stress level is high ({average_stress:.1f}). Stress reduction strategies could improve health.")

        if average_sleep < 6:
            trend_summary.append(f"Average sleep duration is below recommended levels ({average_sleep:.1f} hours). Improving sleep hygiene might help.")

        # Analyzing medication adherence
        missed_medication_logs = self.data[self.data['took_medication'] == False]
        if not missed_medication_logs.empty:
            trend_summary.append(f"Medication was missed on {len(missed_medication_logs)} occasions. Ensure regular medication intake to manage symptoms effectively.")

        return " ".join(trend_summary) if trend_summary else "No significant trends detected."

    def save_trend_analysis(self):
        """
        Save the trend analysis summary for the user in the database.
        """
        trend_summary = self.analyze_trends()

        # Create a new TrendAnalysis entry
        new_trend_analysis = TrendAnalysis(
            user_id=self.user_id,
            analysis_summary=trend_summary,
            generated_at=datetime.utcnow()
        )

        try:
            # Add the new trend analysis to the session and commit
            self.db_session.add(new_trend_analysis)
            self.db_session.commit()
            print(f"Trend analysis successfully saved for user {self.user_id}.")
        except Exception as e:
            self.db_session.rollback()
            print(f"An error occurred while saving trend analysis for user {self.user_id}: {e}")

    def generate_user_trends(self):
        """
        Load user data, perform trend analysis, and save the summary to the database.
        This function is the main entry point to generate and save trends for a user.
        """
        self.load_user_data()
        self.save_trend_analysis()

# Example Usage:
# from flask import current_app
# from sqlalchemy.orm import scoped_session
# db_session = scoped_session(db.session)
# analyzer = TrendAnalyzer(user_id=1, db_session=db_session)
# analyzer.generate_user_trends()
