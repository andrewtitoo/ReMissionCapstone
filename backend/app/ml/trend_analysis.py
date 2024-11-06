import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from .. import db  # Assumes file is within `backend/app/ml/`
from ..models import SymptomLog, TrendAnalysis

class TrendAnalyzer:
    """
    Analyzes trends in user symptom logs for generating insights. Helps CHIIP detect patterns in user data.
    """

    def __init__(self, user_id, db_session: Session):
        """
        Initialize TrendAnalyzer for a specific user.

        Args:
            user_id (int): ID of the user to analyze.
            db_session (Session): SQLAlchemy session for database interactions.
        """
        self.user_id = user_id
        self.db_session = db_session
        self.data = None

    def load_user_data(self):
        """
        Loads historical symptom logs for the user.
        """
        try:
            # Query symptom logs
            symptom_logs = self.db_session.query(SymptomLog).filter_by(user_id=self.user_id).all()
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
            print(f"Error loading data for user {self.user_id}: {e}")

    def analyze_trends(self):
        """
        Analyze user data to identify trends and generate insights.

        Returns:
            str: A summary of detected trends.
        """
        if self.data is None or self.data.empty:
            return "No data available for trend analysis."

        trend_summary = []

        # High pain frequency analysis
        high_pain_logs = self.data[self.data['pain_level'] > 7]
        if not high_pain_logs.empty:
            trend_summary.append(f"High pain levels recorded on {len(high_pain_logs)} occasions. Consider reviewing potential triggers.")

        # Stress and sleep analysis
        average_stress = self.data['stress_level'].mean()
        average_sleep = self.data['sleep_hours'].mean()

        if average_stress > 6:
            trend_summary.append(f"High average stress level ({average_stress:.1f}). Stress reduction might help.")

        if average_sleep < 6:
            trend_summary.append(f"Average sleep duration is low ({average_sleep:.1f} hours). Improving sleep might help.")

        # Medication adherence analysis
        missed_med_logs = self.data[self.data['took_medication'] == False]
        if not missed_med_logs.empty:
            trend_summary.append(f"Medication missed on {len(missed_med_logs)} occasions. Regular intake may improve symptoms.")

        return " ".join(trend_summary) if trend_summary else "No significant trends detected."

    def save_trend_analysis(self):
        """
        Saves the trend analysis summary in the database.
        """
        trend_summary = self.analyze_trends()
        new_trend_analysis = TrendAnalysis(
            user_id=self.user_id,
            analysis_summary=trend_summary,
            generated_at=datetime.utcnow()
        )

        try:
            self.db_session.add(new_trend_analysis)
            self.db_session.commit()
            print(f"Trend analysis saved for user {self.user_id}.")
        except Exception as e:
            self.db_session.rollback()
            print(f"Error saving trend analysis for user {self.user_id}: {e}")

    def generate_user_trends(self):
        """
        Load data, analyze trends, and save summary for the user.
        """
        self.load_user_data()
        self.save_trend_analysis()
