import re

class InputValidator:
    """
    A class to validate and sanitize user inputs for ReMission app.
    This class ensures that all data is in the correct format and meets required constraints.
    """

    @staticmethod
    def validate_pain_level(pain_level):
        """
        Validate the pain level input from the user.

        Args:
            pain_level (int): The pain level input provided by the user (1-10).

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if isinstance(pain_level, int) and 1 <= pain_level <= 10:
            return True
        print(f"Invalid pain level: {pain_level}. Must be an integer between 1 and 10.")
        return False

    @staticmethod
    def validate_stress_level(stress_level):
        """
        Validate the stress level input from the user.

        Args:
            stress_level (int): The stress level input provided by the user (1-10).

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if isinstance(stress_level, int) and 1 <= stress_level <= 10:
            return True
        print(f"Invalid stress level: {stress_level}. Must be an integer between 1 and 10.")
        return False

    @staticmethod
    def validate_sleep_hours(sleep_hours):
        """
        Validate the sleep hours input from the user.

        Args:
            sleep_hours (float): The sleep hours input provided by the user (0-24).

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if isinstance(sleep_hours, (int, float)) and 0 <= sleep_hours <= 24:
            return True
        print(f"Invalid sleep hours: {sleep_hours}. Must be a number between 0 and 24.")
        return False

    @staticmethod
    def validate_diet_triggers(diet_triggers):
        """
        Validate the diet triggers input from the user.

        Args:
            diet_triggers (list of str): A list of food trigger types (e.g., ['dairy', 'spicy']).

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        valid_triggers = {'dairy', 'spicy', 'fried', 'processed', 'gluten'}
        if isinstance(diet_triggers, list) and all(trigger in valid_triggers for trigger in diet_triggers):
            return True
        print(f"Invalid diet triggers: {diet_triggers}. Must be a list containing valid trigger types: {valid_triggers}")
        return False

    @staticmethod
    def validate_medication(took_medication):
        """
        Validate if the user took medication.

        Args:
            took_medication (bool): Whether or not the user took medication.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if isinstance(took_medication, bool):
            return True
        print(f"Invalid medication value: {took_medication}. Must be a boolean (True/False).")
        return False

    @staticmethod
    def validate_exercise_done(exercise_done):
        """
        Validate if the user exercised.

        Args:
            exercise_done (bool): Whether or not the user did exercise.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if isinstance(exercise_done, bool):
            return True
        print(f"Invalid exercise done value: {exercise_done}. Must be a boolean (True/False).")
        return False

    @staticmethod
    def validate_exercise_type(exercise_done, exercise_type):
        """
        Validate the exercise type if the user exercised.

        Args:
            exercise_done (bool): Whether or not the user did exercise.
            exercise_type (str): The type of exercise (e.g., 'cardio', 'strength').

        Returns:
            bool: True if the input is valid or if no exercise was done, False otherwise.
        """
        valid_exercise_types = {'cardio', 'strength', 'flexibility', 'balance'}
        if exercise_done:
            if exercise_type in valid_exercise_types:
                return True
            print(f"Invalid exercise type: {exercise_type}. Must be one of {valid_exercise_types}")
            return False
        return True

# Example Usage:
# valid = InputValidator.validate_pain_level(7)
# if not valid:
#     print("Invalid pain level provided")
