import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

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

        try:
            with open(self.model_file_path, 'rb') as model_file:
                self.pipeline = pickle.load(model_file)
                print("Model loaded successfully from file.")
        except FileNotFoundError:
            self.pipeline = Pipeline(steps=[
                ('preprocessor', None),  # Placeholder, updated in `train_model`.
                ('model', RandomForestClassifier(n_estimators=100, random_state=42))
            ])
            print("No pre-trained model found. Initialized a new RandomForest model.")

    def preprocess_data(self, data):
        """
        Preprocesses input data for prediction.

        Args:
            data (pd.DataFrame): Symptom data to preprocess.

        Returns:
            np.array: Transformed feature array for the model.
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

        return preprocessor.fit_transform(data), preprocessor

    def train_model(self, csv_path='synthetic_data.csv'):
        """
        Trains the model using synthetic or real symptom data.

        Args:
            csv_path (str): Path to the CSV containing training data.
        """
        data = pd.read_csv(csv_path)
        X = data[['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication', 'exercise_type']]
        y = data['flare_up']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_processed, preprocessor = self.preprocess_data(X_train)

        # Update pipeline with preprocessor and train model
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        self.pipeline.fit(X_train, y_train)

        # Evaluate model
        X_test_processed = preprocessor.transform(X_test)
        y_pred = self.pipeline.predict(X_test_processed)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

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
        data = pd.DataFrame([symptom_logs])
        features = self.pipeline['preprocessor'].transform(data)

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
            insights.append("High pain detected. Seek advice.")

        if symptom_logs.get('stress_level', 0) > 6:
            insights.append("High stress. Try relaxation techniques.")

        if not symptom_logs.get('took_medication', True):
            insights.append("Missed medication detected.")

        if not symptom_logs.get('exercise_done', True):
            insights.append("Exercise helps prevent flare-ups.")

        return " ".join(insights)
