-- SQL schema for ReMission database

-- Table for storing user information
-- Simplified to only store a unique user_id and creation timestamp
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Internal identifier (autoincrement)
    user_id VARCHAR(10) UNIQUE NOT NULL, -- Unique 6-digit string User ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Store account creation time
);

-- Table for storing symptom logs reported by users
CREATE TABLE IF NOT EXISTS symptom_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Internal log ID
    user_id VARCHAR(10) NOT NULL, -- References user via their unique User ID
    pain_level INTEGER NOT NULL, -- Scale of 1-10 for pain severity
    stress_level INTEGER NOT NULL, -- Scale of 1-10 for stress
    sleep_hours REAL NOT NULL, -- Number of sleep hours (e.g., 7.5)
    exercise_done BOOLEAN NOT NULL, -- Whether user exercised (true/false)
    exercise_type VARCHAR(50), -- Type of exercise (cardio, strength, etc.)
    took_medication BOOLEAN NOT NULL, -- Whether user took prescribed medication
    diet_notes VARCHAR(500), -- Optional dietary information for the day
    additional_notes VARCHAR(500), -- Any extra information users wish to log
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date & time of log creation
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- Enforce ownership of logs
);

-- Table for storing model predictions
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Internal prediction ID
    user_id VARCHAR(10) NOT NULL, -- Associated User ID
    prediction_result VARCHAR(50) NOT NULL, -- Prediction outcome (e.g., Flare-up, Stable)
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when prediction was generated
    additional_info VARCHAR(500), -- Supporting or explanatory details
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- User linkage
);

-- Table for storing trend analysis summaries for users
CREATE TABLE IF NOT EXISTS trend_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique trend record ID
    user_id VARCHAR(10) NOT NULL, -- The user whose trends are analyzed
    analysis_summary VARCHAR(1000) NOT NULL, -- Summary of the observed trends
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When this analysis was generated
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- Ensure linkage and cascade on user deletion
);
