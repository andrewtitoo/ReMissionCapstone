import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

class FlareUpPredictor:
    """
    Handles flare-up predictions, including data preprocessing,
    model training, and prediction based on user symptom logs.
    """

    def __init__(self):
        """
        Initializes the FlareUpPredictor class.
        Loads a pre-trained model if available; otherwise, initializes a new RandomForest model.
        """
        self.model_file_path = os.path.join(os.path.dirname(__file__), "flare_up_model.pkl")

        try:
            with open(self.model_file_path, 'rb') as model_file:
                self.pipeline = pickle.load(model_file)
                print("[DEBUG] Model loaded successfully from file.")
        except FileNotFoundError:
            print("[DEBUG] No pre-trained model found. Initializing a new model.")
            self.pipeline = None  # Will be set during `train_model`.

    def preprocess_data(self, data):
        """
        Preprocesses input data for prediction.
        """
        categorical_cols = ['exercise_type']
        numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline([
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scaler', StandardScaler())
                ]), numerical_cols),
                ('cat', Pipeline([
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))
                ]), categorical_cols)
            ]
        )

        return preprocessor

    def train_model(self, csv_path):
        """
        Trains the model using synthetic or real symptom data.
        """
        csv_path = os.path.abspath(csv_path)
        print(f"[DEBUG] Resolved CSV path: {csv_path}")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"[ERROR] CSV file not found at: {csv_path}")

        try:
            data = pd.read_csv(csv_path)
            print(f"[DEBUG] CSV loaded successfully with {data.shape[0]} rows and {data.shape[1]} columns.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to read CSV: {e}")

        # Features and target
        X = data[['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication', 'exercise_type']]
        y = data['flare_up']
        print("[DEBUG] Data columns and target extracted successfully.")

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("[DEBUG] Split data into training and testing sets.")

        # Preprocess data
        preprocessor = self.preprocess_data(X_train)
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        self.pipeline.fit(X_train, y_train)
        print("[DEBUG] Model trained successfully.")

        # Test model
        y_pred = self.pipeline.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

        # Save trained model
        with open(self.model_file_path, 'wb') as model_file:
            pickle.dump(self.pipeline, model_file)
            print("[DEBUG] Model saved successfully.")

    def predict_flare_up(self, symptom_logs, user_logs, username='User'):
        """
        Predicts likelihood of a flare-up and provides personalized insights based on trends.
        """
        data = pd.DataFrame([symptom_logs])
        features = self.pipeline['preprocessor'].transform(data)
        prediction = self.pipeline.predict(features)

        suggestion = self.generate_insights(user_logs)

        return {
            'greeting': f"Hello, {username}! Here's what I found based on your recent logs.",
            'flare_up': bool(prediction[0]),
            'suggestion': suggestion
        }

    def generate_insights(self, user_logs):
        """
        Generates insights based on historical symptom data.
        """
        insights = []
        recent_logs = user_logs.tail(5)

        if recent_logs.empty:
            return "Not enough historical data to provide detailed insights. Keep logging!"

        if (recent_logs['sleep_hours'] < 6).sum() >= 3:
            insights.append("Consistently low sleep detected. Prioritize rest.")

        if (recent_logs['took_medication'] == 0).sum() >= 3:
            insights.append("You’ve missed medication multiple times. This may increase risks.")

        if (recent_logs['stress_level'] > 6).sum() >= 3:
            insights.append("High stress levels detected. Consider stress management.")

        if (recent_logs['exercise_done'] == 0).sum() >= 3:
            insights.append("Lack of regular exercise detected.")

        if not insights:
            insights.append("Your logs look stable! Keep maintaining good habits.")

        return " ".join(insights)

if __name__ == "__main__":
    predictor = FlareUpPredictor()
    csv_path = r"D:\ReMission\database\synthetic_data.csv"
    predictor.train_model(csv_path=csv_path)
