PRAGMA foreign_keys = ON;

-- Seed users (passwords are placeholders and not intended for login).
INSERT OR IGNORE INTO users (id, full_name, email, password_hash, created_at) VALUES
(1, 'John Doe', 'john.doe@email.com', 'seed-hash-john', CURRENT_TIMESTAMP),
(2, 'Jane Smith', 'jane.smith@email.com', 'seed-hash-jane', CURRENT_TIMESTAMP),
(3, 'Mike Johnson', 'mike.johnson@email.com', 'seed-hash-mike', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO patient_profiles (user_id, full_name, age, gender, bmi, updated_at) VALUES
(1, 'John Doe', 39, 'male', 27.5, CURRENT_TIMESTAMP),
(2, 'Jane Smith', 34, 'female', 24.1, CURRENT_TIMESTAMP),
(3, 'Mike Johnson', 46, 'male', 31.2, CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO appointments (id, user_id, provider_name, start_time, end_time, reason, status, created_at) VALUES
(1, 1, 'Dr. Williams', '2099-08-10 09:00:00', '2099-08-10 09:30:00', 'Regular diabetes checkup', 'scheduled', CURRENT_TIMESTAMP),
(2, 1, 'Dr. Brown', '2099-09-01 14:00:00', '2099-09-01 14:30:00', 'General checkup', 'scheduled', CURRENT_TIMESTAMP),
(3, 2, 'Dr. Williams', '2099-08-15 11:00:00', '2099-08-15 11:30:00', 'First diabetes consultation', 'scheduled', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO medical_history (id, user_id, condition_name, notes, created_at) VALUES
(1, 1, 'Hypertension', 'Former smoker, elevated blood glucose', CURRENT_TIMESTAMP),
(2, 2, 'Routine Screening', 'No known chronic disease', CURRENT_TIMESTAMP),
(3, 3, 'Diabetes Risk', 'Family history and high BMI', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO predictions (id, user_id, risk_label, risk_score, created_at) VALUES
(1, 1, 'high_risk', 0.87, CURRENT_TIMESTAMP),
(2, 2, 'low_risk', 0.92, CURRENT_TIMESTAMP),
(3, 3, 'high_risk', 0.95, CURRENT_TIMESTAMP);