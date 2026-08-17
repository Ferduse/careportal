-- ============================================
-- HEALTHCARE APP - QUERY REFERENCE FILE
-- For Backend Integration
-- ============================================

-- ============================================
-- USER QUERIES
-- ============================================

-- Register new user
INSERT INTO Users (email, password, role)
VALUES (?, ?, 'patient');

-- Login - check user credentials
SELECT user_id, email, role
FROM Users
WHERE email = ? AND password = ?;

-- Get user by ID
SELECT * FROM Users
WHERE user_id = ?;






-- ============================================
-- PATIENT QUERIES
-- ============================================

-- Create new patient profile after registration
INSERT INTO Patients (user_id, first_name, last_name, date_of_birth, gender, phone, address)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Get patient profile
SELECT p.*, u.email
FROM Patients p
JOIN Users u ON p.user_id = u.user_id
WHERE p.patient_id = ?;

-- Update patient profile
UPDATE Patients
SET first_name = ?, last_name = ?, phone = ?, address = ?
WHERE patient_id = ?;







-- ============================================
-- DOCTOR QUERIES
-- ============================================

-- Get all doctors
SELECT * FROM Doctors;

-- Get doctor by specialization
SELECT * FROM Doctors
WHERE specialization = ?;

-- Get doctor by ID
SELECT * FROM Doctors
WHERE doctor_id = ?;






-- ============================================
-- APPOINTMENT QUERIES
-- ============================================

-- Book new appointment
INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, notes)
VALUES (?, ?, ?, 'scheduled', ?);

-- Get all appointments for a patient
SELECT a.*, d.first_name, d.last_name, d.specialization
FROM Appointments a
JOIN Doctors d ON a.doctor_id = d.doctor_id
WHERE a.patient_id = ?
ORDER BY a.appointment_date DESC;

-- Get upcoming appointments for a patient
SELECT a.*, d.first_name, d.last_name, d.specialization
FROM Appointments a
JOIN Doctors d ON a.doctor_id = d.doctor_id
WHERE a.patient_id = ?
AND a.status = 'scheduled'
AND a.appointment_date >= NOW()
ORDER BY a.appointment_date ASC;

-- Cancel appointment
UPDATE Appointments
SET status = 'cancelled'
WHERE appointment_id = ? AND patient_id = ?;

-- Complete appointment
UPDATE Appointments
SET status = 'completed'
WHERE appointment_id = ?;

-- Get all appointments for a doctor
SELECT a.*, p.first_name, p.last_name
FROM Appointments a
JOIN Patients p ON a.patient_id = p.patient_id
WHERE a.doctor_id = ?
ORDER BY a.appointment_date ASC;







-- ============================================
-- MEDICAL HISTORY QUERIES
-- ============================================

-- Insert new medical history (first time patient fills it in)
INSERT INTO MedicalHistory (patient_id, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose, diagnosis_date)
VALUES (?, ?, ?, ?, ?, ?, ?, NOW());

-- Update existing medical history
UPDATE MedicalHistory
SET hypertension = ?,
    heart_disease = ?,
    smoking_history = ?,
    bmi = ?,
    HbA1c_level = ?,
    blood_glucose = ?,
    diagnosis_date = NOW()
WHERE patient_id = ?;

-- Get medical history for a patient
SELECT * FROM MedicalHistory
WHERE patient_id = ?
ORDER BY diagnosis_date DESC;

-- Get latest medical history entry for a patient
SELECT * FROM MedicalHistory
WHERE patient_id = ?
ORDER BY diagnosis_date DESC
LIMIT 1;





-- ============================================
-- PREDICTION QUERIES
-- ============================================

-- Store new prediction after ML model runs
INSERT INTO Predictions (patient_id, history_id, diabetes, confidence, predicted_date)
VALUES (?, ?, ?, ?, NOW());

-- Get all predictions for a patient
SELECT pr.*, mh.bmi, mh.blood_glucose, mh.HbA1c_level
FROM Predictions pr
JOIN MedicalHistory mh ON pr.history_id = mh.history_id
WHERE pr.patient_id = ?
ORDER BY pr.predicted_date DESC;

-- Get latest prediction for a patient
SELECT pr.*, mh.bmi, mh.blood_glucose, mh.HbA1c_level
FROM Predictions pr
JOIN MedicalHistory mh ON pr.history_id = mh.history_id
WHERE pr.patient_id = ?
ORDER BY pr.predicted_date DESC
LIMIT 1;







-- ============================================
-- DASHBOARD SUMMARY QUERY
-- name: get_user_by_email
SELECT id, full_name, email, password_hash, created_at
FROM users
WHERE email = :email;

-- name: get_refresh_token_by_token
SELECT id, user_id, token, created_at
FROM refresh_tokens
WHERE token = :token;

-- name: get_patient_profile_by_user_id
SELECT user_id, full_name, age, gender, bmi, updated_at
FROM patient_profiles
WHERE user_id = :user_id;

-- name: list_appointments_for_user
SELECT id, user_id, provider_name, start_time, end_time, reason, status, created_at
FROM appointments
WHERE user_id = :user_id
ORDER BY start_time ASC;

-- name: get_appointment_for_user
SELECT id, user_id, provider_name, start_time, end_time, reason, status, created_at
FROM appointments
WHERE id = :appointment_id AND user_id = :user_id;

-- name: find_appointment_conflict
SELECT id, user_id, provider_name, start_time, end_time, reason, status, created_at
FROM appointments
WHERE user_id = :user_id
    AND provider_name = :provider_name
    AND status != 'canceled'
    AND start_time < :end_time
    AND end_time > :start_time
    AND (:skip_id IS NULL OR id != :skip_id)
LIMIT 1;

-- name: list_medical_history_for_user
SELECT id, user_id, condition_name, notes, created_at
FROM medical_history
WHERE user_id = :user_id
ORDER BY created_at DESC;

-- name: get_medical_history_for_user
SELECT id, user_id, condition_name, notes, created_at
FROM medical_history
WHERE id = :record_id AND user_id = :user_id;

-- name: list_predictions_for_user
SELECT id, user_id, risk_label, risk_score, created_at
FROM predictions
WHERE user_id = :user_id
ORDER BY created_at DESC;
