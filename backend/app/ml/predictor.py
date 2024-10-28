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

# Assuming that the Prediction model, User model, and SymptomLog model are imported
from ..models import User, SymptomLog, Prediction

class FlareUpPredictor:
    """
    Class responsible for handling flare-up predictions, including data preprocessing,
    model training, and providing predictions based on user symptom logs.
    """

    def __init__(self):
        """
        Initialize the FlareUpPredictor class.
        Loads the pre-trained model if available, or initializes a new RandomForest model.
        """
        self.model_file_path = "backend/app/ml/flare_up_model.pkl"

        # Load existing model if available, otherwise initialize a new RandomForestClassifier
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
        Preprocesses the data to be used for prediction.

        Args:
            symptom_logs (dict): Dictionary containing user symptom data.

        Returns:
            numpy.array: Processed feature array for the model.
        """
        # Create a DataFrame from the user input for easier preprocessing
        data = pd.DataFrame([symptom_logs])

        # Define categorical and numerical columns
        categorical_cols = ['exercise_type']
        numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        # Define preprocessing steps for numerical and categorical columns
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),  # Fill missing numerical values with mean
            ('scaler', StandardScaler())  # Standardize numerical values
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill missing categorical values with the most frequent value
            ('onehot', OneHotEncoder(handle_unknown='ignore'))  # One-hot encode categorical values
        ])

        # Combine preprocessing for numerical and categorical features
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )

        # Transform the data using the preprocessor
        processed_data = preprocessor.fit_transform(data)
        return processed_data

    def train_model(self, data):
        """
        Train the RandomForest model using the provided data.

        Args:
            data (pd.DataFrame): A DataFrame containing symptom data with labels.
        """
        # Split features and target labels
        X = data[['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication', 'exercise_type']]
        y = data['flare_up']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define categorical and numerical columns for preprocessing
        categorical_cols = ['exercise_type']
        numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        # Define preprocessing pipelines for numerical and categorical columns
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Combine preprocessing for numerical and categorical features
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )

        # Full pipeline with preprocessor and model
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        # Train the model
        self.pipeline.fit(X_train, y_train)

        # Evaluate model performance
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Training Accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))

        # Save the trained model
        with open(self.model_file_path, 'wb') as model_file:
            pickle.dump(self.pipeline, model_file)
            print("Model saved to file.")

    def predict_flare_up(self, symptom_logs):
        """
        Predict the likelihood of a flare-up using user-provided symptom data.

        Args:
            symptom_logs (dict): Dictionary containing user symptom data.

        Returns:
            dict: A dictionary containing the prediction result and probability.
        """
        # Preprocess the input data
        features = self.preprocess_data(symptom_logs)

        # Make a prediction using the trained model
        prediction = self.pipeline.predict(features)
        prediction_prob = self.pipeline.predict_proba(features)[0]

        # Generate insights for the user
        suggestion = self.generate_insights(symptom_logs, prediction)

        # Return the prediction result and suggestions
        return {
            'flare_up': bool(prediction[0]),
            'probability': float(prediction_prob[1]),  # Probability of a flare-up
            'suggestion': suggestion
        }

    def generate_insights(self, symptom_logs, prediction):
        """
        Generate insights and recommendations based on prediction results.

        Args:
            symptom_logs (dict): Dictionary containing user symptom data.
            prediction (array): Model prediction for flare-up.

        Returns:
            str: Suggestion or recommendation for the user.
        """
        # Basic rules-based insights to accompany the ML prediction
        insights = []

        if symptom_logs.get('pain_level', 0) > 7:
            insights.append("It seems your pain level is quite high. Consider consulting your healthcare provider.")

        if symptom_logs.get('stress_level', 0) > 6:
            insights.append("High stress levels may contribute to your symptoms. Consider stress management techniques like meditation or breathing exercises.")

        if not symptom_logs.get('took_medication', True):
            insights.append("It looks like you haven't taken your medication. Missing doses could be a factor in symptom flare-ups.")

        if not symptom_logs.get('exercise_done', True):
            insights.append("Regular light exercise may help reduce symptoms. Consider adding light physical activities to your routine.")

        return " ".join(insights)

