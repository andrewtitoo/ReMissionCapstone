import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class DataPreprocessor:
    """
    A class to perform data preprocessing for symptom logs.
    Provides methods to preprocess both numerical and categorical data, preparing it for machine learning models or trend analysis.
    """

    def __init__(self):
        """
        Initialize the DataPreprocessor with pipelines for both numerical and categorical data.
        """
        # Define columns for preprocessing
        self.categorical_cols = ['exercise_type']
        self.numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        # Numerical data preprocessing: imputing and scaling
        self.numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        # Categorical data preprocessing: imputing and one-hot encoding
        self.categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Combined preprocessor using ColumnTransformer
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', self.numerical_transformer, self.numerical_cols),
                ('cat', self.categorical_transformer, self.categorical_cols)
            ]
        )

    def preprocess(self, symptom_logs):
        """
        Preprocess user symptom logs.

        Args:
            symptom_logs (list of dicts or pd.DataFrame): User symptom logs.

        Returns:
            np.array: Preprocessed feature array for model input.
        """
        # Convert input to DataFrame if needed
        data = pd.DataFrame(symptom_logs) if isinstance(symptom_logs, list) else symptom_logs

        # Ensure required columns are present
        missing_cols = [col for col in (self.numerical_cols + self.categorical_cols) if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        return self.preprocessor.fit_transform(data)

    def transform_new_data(self, symptom_logs):
        """
        Transform new user symptom logs using existing preprocessor.

        Args:
            symptom_logs (list of dicts or pd.DataFrame): New user symptom logs.

        Returns:
            np.array: Transformed feature array.
        """
        data = pd.DataFrame(symptom_logs) if isinstance(symptom_logs, list) else symptom_logs

        # Check required columns
        missing_cols = [col for col in (self.numerical_cols + self.categorical_cols) if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        return self.preprocessor.transform(data)
