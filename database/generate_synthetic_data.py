import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker to generate realistic random data
fake = Faker()

# Connect to the remission.db SQLite database
conn = sqlite3.connect('remission.db')
cursor = conn.cursor()

# Clear tables before populating to avoid duplicates
cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM symptom_logs")
cursor.execute("DELETE FROM predictions")
cursor.execute("DELETE FROM trend_analysis")
conn.commit()

# Generate synthetic users with unique usernames and emails
def generate_users(n):
    usernames = set()
    emails = set()
    users_added = 0

    while users_added < n:
        username = fake.user_name()
        email = fake.email()

        while username in usernames:
            username = fake.user_name()
        while email in emails:
            email = fake.email()

        password_hash = fake.sha256()
        created_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')

        try:
            cursor.execute("INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                           (username, email, password_hash, created_at))
            conn.commit()
            usernames.add(username)
            emails.add(email)
            users_added += 1
        except sqlite3.IntegrityError:
            print("Duplicate found in database. Retrying with a new username/email.")

generate_users(1000)

# Generate synthetic symptom logs with realistic IBD patterns
def generate_symptom_logs(user_ids, n):
    symptom_logs = []
    for user_id in user_ids:
        for _ in range(n):
            # Determine pain level based on IBD-related factors
            stress_level = random.randint(1, 10)
            sleep_hours = round(random.uniform(4.0, 9.0), 1)
            exercise_done = random.choice([1, 0])
            took_medication = random.choice([1, 0])

            # Determine pain level based on stress, sleep, and medication adherence
            if stress_level >= 8 or sleep_hours < 5:
                pain_level = random.randint(7, 10)  # High pain if stress is high or sleep is very low
            elif stress_level >= 5 and sleep_hours < 7:
                pain_level = random.randint(4, 8)  # Moderate pain for moderate stress and low sleep
            else:
                pain_level = random.randint(1, 5)  # Low pain if stress and sleep are good

            # Encourage exercise and medication adherence to have a positive effect
            if exercise_done:
                pain_level = max(1, pain_level - random.randint(1, 2))  # Reduce pain slightly if exercised
            if took_medication:
                pain_level = max(1, pain_level - random.randint(1, 3))  # Reduce pain more if medication taken

            # Set exercise type if exercise was done
            exercise_type = random.choice(['cardio', 'strength', 'yoga', 'running', None]) if exercise_done else None

            # Generate log timestamps and optional notes
            diet_notes = fake.sentence(nb_words=6)  # Random gibberish notes for now
            additional_notes = fake.sentence(nb_words=8)  # Random gibberish notes for now
            logged_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            timestamp = fake.time()

            symptom_logs.append((user_id, pain_level, stress_level, sleep_hours, exercise_done, exercise_type, took_medication, diet_notes, additional_notes, logged_at, timestamp))

    cursor.executemany("INSERT INTO symptom_logs (user_id, pain_level, stress_level, sleep_hours, exercise_done, exercise_type, took_medication, diet_notes, additional_notes, logged_at, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", symptom_logs)
    conn.commit()

# Generate synthetic predictions based on trends
def generate_predictions(user_ids, n):
    predictions = []
    for user_id in user_ids:
        for _ in range(n):
            # Simulate basic prediction logic based on patterns in the data
            prediction_result = random.choice(['Stable', 'Flare-up Likely'])
            predicted_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            additional_info = "Based on recent logs, keep stress low and ensure adequate sleep to prevent flare-ups."

            if prediction_result == 'Flare-up Likely':
                additional_info = "High pain and stress detected. Rest and consider avoiding trigger foods."

            predictions.append((user_id, prediction_result, predicted_at, additional_info))

    cursor.executemany("INSERT INTO predictions (user_id, prediction_result, predicted_at, additional_info) VALUES (?, ?, ?, ?)", predictions)
    conn.commit()

# Generate synthetic trend analysis for insights over time
def generate_trend_analysis(user_ids, n):
    trends = []
    for user_id in user_ids:
        for _ in range(n):
            analysis_summary = "Trends indicate that high stress and low sleep contribute to flare-ups. Exercise and medication adherence reduce symptoms."
            generated_at = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            trends.append((user_id, analysis_summary, generated_at))

    cursor.executemany("INSERT INTO trend_analysis (user_id, analysis_summary, generated_at) VALUES (?, ?, ?)", trends)
    conn.commit()

# Main function to generate data
def main():
    num_users = 1000  # Number of users
    logs_per_user = 20  # Number of symptom logs per user
    predictions_per_user = 5  # Number of predictions per user
    trends_per_user = 2  # Number of trend analyses per user

    # Generate users and retrieve their IDs
    generate_users(num_users)
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Debugging: Print counts
    cursor.execute("SELECT COUNT(*) FROM users")
    print("Number of users in database:", cursor.fetchone()[0])

    # Generate data for each table based on user IDs
    generate_symptom_logs(user_ids, logs_per_user)
    cursor.execute("SELECT COUNT(*) FROM symptom_logs")
    print("Number of symptom logs in database:", cursor.fetchone()[0])

    generate_predictions(user_ids, predictions_per_user)
    cursor.execute("SELECT COUNT(*) FROM predictions")
    print("Number of predictions in database:", cursor.fetchone()[0])

    generate_trend_analysis(user_ids, trends_per_user)
    cursor.execute("SELECT COUNT(*) FROM trend_analysis")
    print("Number of trend analyses in database:", cursor.fetchone()[0])

    print("Data generation complete!")

if __name__ == "__main__":
    main()
    conn.close()
