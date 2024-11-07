import sqlite3
import random
from datetime import datetime
from faker import Faker
import pandas as pd

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

# Generate synthetic symptom logs with realistic IBD patterns and flare logic
def generate_symptom_logs(user_ids, n):
    symptom_logs = []
    for user_id in user_ids:
        for _ in range(n):
            stress_level = random.randint(1, 10)
            sleep_hours = round(random.uniform(4.0, 9.0), 1)
            exercise_done = random.choice([1, 0])
            took_medication = random.choice([1, 0])
            pain_level = random.randint(1, 10)

            # Define logic for determining flare-up
            flare = 0
            if pain_level >= 7:
                flare = 1
            elif 5 <= pain_level < 7 and (
                    sleep_hours < 7 or took_medication == 0 or stress_level > 5):
                flare = 1
            elif 2 <= pain_level < 5 and (
                    sum([sleep_hours < 7, took_medication == 0, exercise_done == 0, stress_level > 6]) >= 3):
                flare = 1

            exercise_type = random.choice(['cardio', 'strength', 'yoga', 'running', None]) if exercise_done else None

            log_entry = {
                "user_id": user_id,
                "pain_level": pain_level,
                "stress_level": stress_level,
                "sleep_hours": sleep_hours,
                "exercise_done": exercise_done,
                "exercise_type": exercise_type,
                "took_medication": took_medication,
                "flare_up": flare,  # Binary label
                "logged_at": fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            }

            symptom_logs.append(log_entry)

    return symptom_logs

def export_to_csv(symptom_logs):
    df = pd.DataFrame(symptom_logs)
    df.to_csv('synthetic_data.csv', index=False)
    print("Synthetic data exported to synthetic_data.csv")

def main():
    num_users = 1000
    logs_per_user = 20

    generate_users(num_users)
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    symptom_logs = generate_symptom_logs(user_ids, logs_per_user)
    export_to_csv(symptom_logs)

    print("Data generation complete!")

if __name__ == "__main__":
    main()
    conn.close()
