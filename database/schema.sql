-- SQL schema for ReMission database

-- Table for sharing user information
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing symptom logs reported by users
CREATE TABLE symptom_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    pain_level INTEGER NOT NULL, --Scale of 1-10
    stress_level INTEGER NOT NULL, --Scale of 1-10
    sleep_hours REAL NOT NULL, --Number of sleep hours
    exercise_done BOOLEAN NOT NULL, --Yes/No for exercise
    exercise_type VARCHAR(50), --Type of exercise (e.g. cardio, strength)
    took_medication BOOLEAN NOT NULL, --Yes/No for medication intake
    diet_notes VARCHAR(500), --Optional notes on diet for that day
    additional_notes VARCHAR(500), --Additional notes for context
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --Timestamp of Log Creation
    timestamp TIME DEFAULT CURRENT_TIME, --Time of day when entry was made
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Table for storing model predictions
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    prediction_result VARCHAR(50) NOT NULL, -- Example: "Flare-up likely" or "Stable"
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --Timestamp of prediction creation
    additional_info VARCHAR(500), --Additional information or suggestions
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Table for storing trend analysis based on user data
CREATE TABLE trend_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    analysis_summary VARCHAR(1000) NOT NULL, --Summary of trend analysis
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, --Timestamp of trend analysis generation
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);