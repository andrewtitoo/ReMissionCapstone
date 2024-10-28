import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class DataPreprocessor:
    """
    A class to perform data preprocessing for symptom logs.
    This class provides methods to preprocess both numerical and categorical data, preparing it for machine learning models or trend analysis.
    """

    def __init__(self):
        """
        Initialize the DataPreprocessor with preprocessing pipelines for both numerical
        and categorical data.
        """
        # Define categorical and numerical columns
        self.categorical_cols = ['exercise_type']
        self.numerical_cols = ['pain_level', 'stress_level', 'sleep_hours', 'exercise_done', 'took_medication']

        # Preprocessing for numerical data: imputing missing values with mean and scaling
        self.numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),  # Impute missing numerical values with the mean
            ('scaler', StandardScaler())  # Standardize numerical features
        ])

        # Preprocessing for categorical data: imputing missing values with the most frequent and one-hot encoding
        self.categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing categorical values
            ('onehot', OneHotEncoder(handle_unknown='ignore'))  # One-hot encode categorical features
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
            symptom_logs (list of dicts or pandas.DataFrame): User symptom logs as a list of dictionaries or a DataFrame.

        Returns:
            numpy.array: Preprocessed feature array suitable for machine learning models.
        """
        # Convert the input to a DataFrame if it is not already
        if isinstance(symptom_logs, list):
            data = pd.DataFrame(symptom_logs)
        elif isinstance(symptom_logs, pd.DataFrame):
            data = symptom_logs
        else:
            raise ValueError("Input symptom_logs must be a list of dictionaries or a pandas DataFrame.")

        # Ensure that all required columns are present in the DataFrame
        missing_columns = [col for col in (self.numerical_cols + self.categorical_cols) if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns for preprocessing: {missing_columns}")

        # Fit and transform the data using the preprocessor
        processed_data = self.preprocessor.fit_transform(data)

        return processed_data

    def transform_new_data(self, symptom_logs):
        """
        Transform new user symptom logs using the existing fitted preprocessors.
        This function can be used to transform new data after the preprocessor is already trained.

        Args:
            symptom_logs (list of dicts or pandas.DataFrame): New user symptom logs to be transformed.

        Returns:
            numpy.array: Transformed feature array.
        """
        # Convert the input to a DataFrame if it is not already
        if isinstance(symptom_logs, list):
            data = pd.DataFrame(symptom_logs)
        elif isinstance(symptom_logs, pd.DataFrame):
            data = symptom_logs
        else:
            raise ValueError("Input symptom_logs must be a list of dictionaries or a pandas DataFrame.")

        # Ensure that all required columns are present in the DataFrame
        missing_columns = [col for col in (self.numerical_cols + self.categorical_cols) if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns for transformation: {missing_columns}")

        # Transform the data using the fitted preprocessor
        processed_data = self.preprocessor.transform(data)

        return processed_data

# Example Usage:
# preprocessor = DataPreprocessor()
# symptom_logs = [
#     {
#         "pain_level": 8,
#         "stress_level": 7,
#         "sleep_hours": 5.5,
#         "exercise_done": 1,
#         "took_medication": 1,
#         "exercise_type": "cardio"
#     },
#     {
#         "pain_level": 4,
#         "stress_level": 5,
#         "sleep_hours": 7.0,
#         "exercise_done": 0,
#         "took_medication": 1,
#         "exercise_type": "strength"
#     }
# ]
# processed_data = preprocessor.preprocess(symptom_logs)
# print(processed_data)