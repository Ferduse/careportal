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
-- ============================================

-- Get full patient dashboard summary
SELECT
    p.first_name,
    p.last_name,
    COUNT(DISTINCT a.appointment_id) as total_appointments,
    SUM(CASE WHEN a.status = 'scheduled' THEN 1 ELSE 0 END) as upcoming_appointments,
    SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_appointments,
    pr.diabetes as latest_diabetes_prediction,
    pr.confidence as latest_confidence,
    pr.predicted_date as last_prediction_date
FROM Patients p
LEFT JOIN Appointments a ON p.patient_id = a.patient_id
LEFT JOIN Predictions pr ON p.patient_id = pr.patient_id
WHERE p.patient_id = ?
GROUP BY p.patient_id
ORDER BY pr.predicted_date DESC
LIMIT 1;
