import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker to generate realistic random data
fake = Faker()

# Connect to the remission.db SQLite database
conn = sqlite3.connect('remission.db')
cursor = conn.cursor()

# Generate synthetic users
def generate_users(n):
    """
    Generates n users with random usernames, emails, and password hashes.

    Args:
        n (int): Number of users to generate.
    """
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password_hash = fake.sha256()
        created_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        users.append((username, email, password_hash, created_at))
    cursor.executemany("INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)", users)
    conn.commit()

# Generate synthetic symptom logs
def generate_symptom_logs(user_ids, n):
    """
    Generates n symptom logs for each user in user_ids.

    Args:
        user_ids (list): List of user IDs to create logs for.
        n (int): Number of logs per user.
    """
    symptom_logs = []
    for user_id in user_ids:
        for _ in range(n):
            pain_level = random.randint(1, 10)
            stress_level = random.randint(1, 10)
            sleep_hours = round(random.uniform(4.0, 9.0), 1)
            exercise_done = random.choice([0, 1])
            exercise_type = random.choice(['cardio', 'strength', 'yoga', 'running', None]) if exercise_done else None
            took_medication = random.choice([0, 1])
            diet_notes = fake.sentence(nb_words=6)
            additional_notes = fake.sentence(nb_words=8)
            logged_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            timestamp = fake.time().strftime('%H:%M:%S')
            symptom_logs.append((user_id, pain_level, stress_level, sleep_hours, exercise_done, exercise_type, took_medication, diet_notes, additional_notes, logged_at, timestamp))
    cursor.executemany("INSERT INTO symptom_logs (user_id, pain_level, stress_level, sleep_hours, exercise_done, exercise_type, took_medication, diet_notes, additional_notes, logged_at, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", symptom_logs)
    conn.commit()

# Generate synthetic predictions
def generate_predictions(user_ids, n):
    """
    Generates n predictions for each user in user_ids.

    Args:
        user_ids (list): List of user IDs to create predictions for.
        n (int): Number of predictions per user.
    """
    predictions = []
    for user_id in user_ids:
        for _ in range(n):
            prediction_result = random.choice(['Stable', 'Flare-up Likely'])
            predicted_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            additional_info = fake.sentence(nb_words=10)
            predictions.append((user_id, prediction_result, predicted_at, additional_info))
    cursor.executemany("INSERT INTO predictions (user_id, prediction_result, predicted_at, additional_info) VALUES (?, ?, ?, ?)", predictions)
    conn.commit()

# Generate synthetic trend analysis
def generate_trend_analysis(user_ids, n):
    """
    Generates n trend analyses for each user in user_ids.

    Args:
        user_ids (list): List of user IDs to create trend analyses for.
        n (int): Number of trend analyses per user.
    """
    trends = []
    for user_id in user_ids:
        for _ in range(n):
            analysis_summary = fake.paragraph(nb_sentences=3)
            generated_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            trends.append((user_id, analysis_summary, generated_at))
    cursor.executemany("INSERT INTO trend_analysis (user_id, analysis_summary, generated_at) VALUES (?, ?, ?)", trends)
    conn.commit()

# Main function to generate data
def main():
    num_users = 1000  # Generate data for 1000 users
    logs_per_user = 20  # Number of symptom logs per user
    predictions_per_user = 5  # Number of predictions per user
    trends_per_user = 2  # Number of trend analyses per user

    # Generate users and retrieve their IDs
    generate_users(num_users)
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Generate data for each table based on user IDs
    generate_symptom_logs(user_ids, logs_per_user)
    generate_predictions(user_ids, predictions_per_user)
    generate_trend_analysis(user_ids, trends_per_user)
    print("Data generation complete!")

if __name__ == "__main__":
    main()
    conn.close()
