import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Assuming necessary imports from the models and database
from ..models import User, SymptomLog, Prediction

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
        self.model_file_path = "backend/app/ml/flare_up_model.pkl"

        # Load existing model if available; otherwise, create a new RandomForest model
        try:
            with open(self.model_file_path, 'rb') as model_file:
                self.pipeline = pickle.load(model_file)
                print("Model loaded successfully from file.")
        except FileNotFoundError:
            self.pipeline = Pipeline(steps=[
                ('model', RandomForestClassifier(n_estimators=100, random_state=42))
            ])
            print("No pre-trained model found. Initialized a new RandomForest model.")

    def preprocess_data(self, symptom_logs):
        """
        Preprocesses data for prediction.

        Args:
            symptom_logs (dict): Dictionary of user symptom data.

        Returns:
            np.array: Processed feature array for the model.
        """
        data = pd.DataFrame([symptom_logs])

        # Define columns
        categorical_cols = ['exercise_type']
        numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        # Define preprocessing steps
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Combine preprocessing
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )

        processed_data = preprocessor.fit_transform(data)
        return processed_data

    def train_model(self, data):
        """
        Trains the model using provided data.

        Args:
            data (pd.DataFrame): Symptom data with labels.
        """
        X = data[['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication', 'exercise_type']]
        y = data['flare_up']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define columns
        categorical_cols = ['exercise_type']
        numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        # Preprocessing pipelines
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Complete pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )

        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        self.pipeline.fit(X_train, y_train)

        # Model evaluation
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Training Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))

        # Save model
        with open(self.model_file_path, 'wb') as model_file:
            pickle.dump(self.pipeline, model_file)
            print("Model saved.")

    def predict_flare_up(self, symptom_logs):
        """
        Predicts likelihood of a flare-up.

        Args:
            symptom_logs (dict): User symptom data.

        Returns:
            dict: Prediction result and probability.
        """
        features = self.preprocess_data(symptom_logs)

        prediction = self.pipeline.predict(features)
        prediction_prob = self.pipeline.predict_proba(features)[0]

        suggestion = self.generate_insights(symptom_logs, prediction)

        return {
            'flare_up': bool(prediction[0]),
            'probability': float(prediction_prob[1]),
            'suggestion': suggestion
        }

    def generate_insights(self, symptom_logs, prediction):
        """
        Generates insights based on prediction results.

        Args:
            symptom_logs (dict): User symptom data.
            prediction (array): Model prediction.

        Returns:
            str: User suggestions.
        """
        insights = []

        if symptom_logs.get('pain_level', 0) > 7:
            insights.append("Pain level is high. Consult your healthcare provider.")

        if symptom_logs.get('stress_level', 0) > 6:
            insights.append("High stress detected. Consider stress management techniques.")

        if not symptom_logs.get('took_medication', True):
            insights.append("Missed medication may increase flare-up risk.")

        if not symptom_logs.get('exercise_done', True):
            insights.append("Regular light exercise can improve symptoms.")

        return " ".join(insights)
