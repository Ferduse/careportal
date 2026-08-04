-- ============================================
-- SAMPLE DATA FOR CarePortal_backend
-- ============================================

-- 1. USERS FIRST
INSERT INTO Users (email, password_hash, role) VALUES
('john.doe@email.com', 'hashed123', 'patient'),
('jane.smith@email.com', 'hashed456', 'patient'),
('mike.johnson@email.com', 'hashed789', 'patient'),
('dr.williams@hospital.com', 'hashed111', 'doctor'),
('dr.brown@hospital.com', 'hashed222', 'doctor');

-- 2. DOCTORS SECOND
INSERT INTO Doctors (first_name, last_name, specialization, email, phone) VALUES
('Sarah', 'Williams', 'Endocrinology', 'dr.williams@hospital.com', '555-0101'),
('Michael', 'Brown', 'General Practice', 'dr.brown@hospital.com', '555-0102');

-- 3. PATIENTS THIRD
INSERT INTO Patients (user_id, first_name, last_name, date_of_birth, gender, phone, address) VALUES
(1, 'John', 'Doe', '1985-03-15', 'male', '555-1001', '123 Main St'),
(2, 'Jane', 'Smith', '1990-07-22', 'female', '555-1002', '456 Oak Ave'),
(3, 'Mike', 'Johnson', '1978-11-30', 'male', '555-1003', '789 Pine Rd');

-- 4. APPOINTMENTS
INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, notes) VALUES
(1, 1, '2025-08-10 09:00:00', 'scheduled', 'Regular diabetes checkup'),
(1, 2, '2025-07-01 14:00:00', 'completed', 'General checkup completed'),
(2, 1, '2025-08-15 11:00:00', 'scheduled', 'First diabetes consultation'),
(3, 2, '2025-07-20 10:00:00', 'cancelled', 'Patient cancelled'),
(2, 2, '2025-08-20 13:00:00', 'scheduled', 'Follow up appointment');

-- 5. MEDICAL HISTORY
INSERT INTO MedicalHistory (patient_id, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, diagnosis_date) VALUES
(1, 1, 0, 'former', 27.50, 6.80, 145, '2025-06-01'),
(2, 0, 0, 'never', 24.10, 5.20, 98, '2025-06-15'),
(3, 1, 1, 'current', 31.20, 7.50, 180, '2025-06-20');

-- 6. PREDICTIONS LAST
INSERT INTO Predictions (patient_id, history_id, diabetes, confidence) VALUES
(1, 1, 1, 0.87),
(2, 2, 0, 0.92),
(3, 3, 1, 0.95);