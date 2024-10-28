from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import User, SymptomLog, Prediction, TrendAnalysis
from .. import db

def add_record(record, db_session: Session):
    """
    Add a new record to the database.

    Args:
        record (db.Model): An instance of a SQLAlchemy model representing the record to add.
        db_session (Session): SQLAlchemy session for database interactions.

    Returns:
        bool: True if the record is successfully added, False otherwise.
    """
    try:
        db_session.add(record)
        db_session.commit()
        print(f"Record successfully added: {record}")
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error adding record: {e}")
        return False

def get_user_by_id(user_id, db_session: Session):
    """
    Get a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db_session (Session): SQLAlchemy session for database interactions.

    Returns:
        User or None: The User object if found, otherwise None.
    """
    try:
        user = db_session.query(User).get(user_id)
        if user:
            print(f"User found: {user}")
        else:
            print(f"No user found with ID: {user_id}")
        return user
    except SQLAlchemyError as e:
        print(f"Error retrieving user with ID {user_id}: {e}")
        return None

def get_symptom_logs_by_user(user_id, db_session: Session):
    """
    Get all symptom logs for a specific user.

    Args:
        user_id (int): The ID of the user whose logs to retrieve.
        db_session (Session): SQLAlchemy session for database interactions.

    Returns:
        list: A list of SymptomLog objects, or an empty list if none are found.
    """
    try:
        symptom_logs = db_session.query(SymptomLog).filter_by(user_id=user_id).all()
        print(f"Found {len(symptom_logs)} symptom logs for user {user_id}")
        return symptom_logs
    except SQLAlchemyError as e:
        print(f"Error retrieving symptom logs for user {user_id}: {e}")
        return []

def update_record(record, db_session: Session):
    """
    Update an existing record in the database.

    Args:
        record (db.Model): An instance of a SQLAlchemy model representing the record to update.
        db_session (Session): SQLAlchemy session for database interactions.

    Returns:
        bool: True if the record is successfully updated, False otherwise.
    """
    try:
        db_session.commit()
        print(f"Record successfully updated: {record}")
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error updating record: {e}")
        return False

def delete_record(record, db_session: Session):
    """
    Delete a record from the database.

    Args:
        record (db.Model): An instance of a SQLAlchemy model representing the record to delete.
        db_session (Session): SQLAlchemy session for database interactions.

    Returns:
        bool: True if the record is successfully deleted, False otherwise.
    """
    try:
        db_session.delete(record)
        db_session.commit()
        print(f"Record successfully deleted: {record}")
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error deleting record: {e}")
        return False

# Example usage:
# db_session = scoped_session(db.session)
# user = get_user_by_id(1, db_session)
