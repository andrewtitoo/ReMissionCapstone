-- Seed data for ReMission database

-- Insert sample users
INSERT INTO users (username, email, password_hash, created_at)
VALUES
    ('john_doe', 'john@example.com', 'hashed_password_1', '2024-01-01 10:00:00'),
    ('jane_smith', 'jane@example.com', 'hashed_password_2', '2024-01-05 11:30:00'),
    ('bob_brown', 'bob@example.com', 'hashed_password_3', '2024-01-10 09:45:00');

-- Insert sample symptom logs
INSERT INTO symptom_logs (user_id, pain_level, stress_level, sleep_hours, exercise_done, exercise_type, took_medication, diet_notes, additional_notes, logged_at, timestamp)
VALUES
    (1, 7, 6, 6.5, 1, 'cardio', 1, 'Avoided spicy food', 'Mild abdominal pain', '2024-01-02 08:00:00', '08:00:00'),
    (1, 5, 4, 7.0, 1, 'strength', 0, 'Ate dairy', 'Felt low energy', '2024-01-03 09:15:00', '09:15:00'),
    (2, 3, 3, 8.0, 1, 'yoga', 1, 'Vegetarian diet', 'Good energy level', '2024-01-06 07:30:00', '07:30:00'),
    (2, 6, 5, 5.5, 0, NULL, 1, 'Ate fried food', 'Mild discomfort', '2024-01-07 10:45:00', '10:45:00'),
    (3, 8, 7, 6.0, 1, 'running', 0, 'Skipped breakfast', 'Severe cramps', '2024-01-11 12:00:00', '12:00:00'),
    (3, 4, 2, 7.5, 1, 'cardio', 1, 'Balanced diet', 'Slight discomfort', '2024-01-12 08:30:00', '08:30:00');

-- Insert sample predictions
INSERT INTO predictions (user_id, prediction_result, predicted_at, additional_info)
VALUES
    (1, 'Stable', '2024-01-02 08:05:00', 'No flare-ups expected in the next 24 hours'),
    (1, 'Flare-up Likely', '2024-01-03 09:20:00', 'High-stress levels; recommended to rest and avoid spicy food'),
    (2, 'Stable', '2024-01-06 07:35:00', 'Maintain current routine for stable health'),
    (2, 'Flare-up Likely', '2024-01-07 10:50:00', 'Symptoms may worsen due to fried food intake'),
    (3, 'Flare-up Likely', '2024-01-11 12:05:00', 'Symptoms likely due to skipped meal'),
    (3, 'Stable', '2024-01-12 08:35:00', 'Balanced diet likely contributing to stable health');

-- Insert sample trend analysis
INSERT INTO trend_analysis (user_id, analysis_summary, generated_at)
VALUES
    (1, 'Increased pain observed when stress levels are above 5. Symptoms improved with consistent sleep over 7 hours.', '2024-01-05 12:00:00'),
    (2, 'Symptoms improved with a vegetarian diet. Flare-ups more likely with fried food.', '2024-01-08 13:45:00'),
    (3, 'Skipping meals correlates with increased symptom severity. Consistent exercise improves symptoms.', '2024-01-15 10:30:00');
