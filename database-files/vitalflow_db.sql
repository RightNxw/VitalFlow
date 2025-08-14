DROP DATABASE IF EXISTS vitalflow_database;
CREATE DATABASE IF NOT EXISTS vitalflow_database;

USE vitalflow_database;

CREATE TABLE IF NOT EXISTS Doctor (
    DoctorID INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Specialty VARCHAR(80),
    YearOfExperience INTEGER
);

CREATE TABLE IF NOT EXISTS Nurse (
    NurseID INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Insurance (
    InsuranceID INTEGER PRIMARY KEY AUTO_INCREMENT,
    InsuranceProvider VARCHAR(100) NOT NULL,
    PolicyNumber VARCHAR(50) NOT NULL,
    Deductible DECIMAL(10,2),
    DueDate DATE
);

CREATE TABLE IF NOT EXISTS Visits (
    VisitID INTEGER PRIMARY KEY AUTO_INCREMENT,
    AdmitReason TEXT,
    AppointmentDate DATE NOT NULL,
    NextVisitDate DATE,
    INDEX idx_visit_date (AppointmentDate)
);

CREATE TABLE IF NOT EXISTS VitalChart (
    VitalID INTEGER PRIMARY KEY AUTO_INCREMENT,
    HeartRate INTEGER,
    BloodPressure VARCHAR(20),
    RespiratoryRate INTEGER,
    Temperature DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS `Condition` (
    ConditionID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Description TEXT NOT NULL,
    Treatment TEXT
);

CREATE TABLE IF NOT EXISTS Discharge (
    DischargeID INTEGER PRIMARY KEY AUTO_INCREMENT,
    DischargeDate DATE DEFAULT (CURRENT_DATE),
    Instructions TEXT,
    INDEX idx_discharge_date (DischargeDate)
);

CREATE TABLE IF NOT EXISTS Patient (
    PatientID INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DOB DATE NOT NULL,
    Weight DECIMAL(6,2),
    BloodType VARCHAR(10),
    PreExisting BOOLEAN,
    InsuranceID INTEGER,
    DischargeID INTEGER,
    ConditionID INTEGER,
    DoctorID INTEGER,
    NurseID INTEGER,
    VitalID INTEGER,
    VisitID INTEGER,
    FOREIGN KEY (InsuranceID) REFERENCES Insurance(InsuranceID),
    FOREIGN KEY (DischargeID) REFERENCES Discharge(DischargeID),
    FOREIGN KEY (ConditionID) REFERENCES `Condition`(ConditionID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID),
    FOREIGN KEY (VitalID) REFERENCES VitalChart(VitalID),
    FOREIGN KEY (VisitID) REFERENCES Visits(VisitID),
    INDEX idx_patient_doctor (DoctorID),
    INDEX idx_patient_nurse (NurseID),
    INDEX idx_patient_insurance (InsuranceID),
    INDEX idx_patient_discharge (DischargeID),
    INDEX idx_patient_condition (ConditionID),
    INDEX idx_patient_visit (VisitID),
    INDEX idx_patient_vital (VitalID)
);

CREATE TABLE IF NOT EXISTS Proxy (
    ProxyID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PatientID INTEGER NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Relationship VARCHAR(50),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
    INDEX idx_proxy_patient (PatientID)
);

CREATE TABLE IF NOT EXISTS Medication (
    MedicationID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PrescriptionName VARCHAR(100) NOT NULL,
    DosageAmount DECIMAL(10,2),
    DosageUnit VARCHAR(20),
    PickUpLocation VARCHAR(100),
    RefillsLeft INTEGER,
    FrequencyAmount INTEGER,
    FrequencyPeriod VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Patient_Medications (
    PatientID INTEGER,
    MedicationID INTEGER,
    PrescribedDate DATE DEFAULT (CURRENT_DATE),
    EndDate DATE,
    PRIMARY KEY (PatientID, MedicationID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID),
    INDEX idx_patient_meds_patient (PatientID),
    INDEX idx_patient_meds_medication (MedicationID),
    INDEX idx_patient_meds_date (PrescribedDate)
);

CREATE TABLE IF NOT EXISTS MessageDetails (
    MessageID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Subject VARCHAR(255) NOT NULL,
    Content TEXT NOT NULL,
    SentTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PostedBy INTEGER NOT NULL,
    PostedByRole VARCHAR(20),
    SenderType VARCHAR(50),
    ReadStatus BOOLEAN DEFAULT FALSE,
    Priority VARCHAR(20) DEFAULT 'Normal',
    INDEX idx_msg_senttime (SentTime),
    INDEX idx_msg_postedby (PostedBy, PostedByRole)
);

CREATE TABLE IF NOT EXISTS MessagePatients (
    MessageID INTEGER,
    PatientID INTEGER,
    PRIMARY KEY (MessageID, PatientID),
    FOREIGN KEY (MessageID) REFERENCES MessageDetails(MessageID) ON DELETE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
    INDEX idx_msg_patient (PatientID)
);

CREATE TABLE IF NOT EXISTS MessageDoctor (
    MessageID INTEGER,
    DoctorID INTEGER,
    PRIMARY KEY (MessageID, DoctorID),
    FOREIGN KEY (MessageID) REFERENCES MessageDetails(MessageID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID) ON DELETE CASCADE,
    INDEX idx_msg_doctor (DoctorID)
);

CREATE TABLE IF NOT EXISTS MessageNurse (
    MessageID INTEGER,
    NurseID INTEGER,
    PRIMARY KEY (MessageID, NurseID),
    FOREIGN KEY (MessageID) REFERENCES MessageDetails(MessageID) ON DELETE CASCADE,
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE,
    INDEX idx_msg_nurse (NurseID)
);

CREATE TABLE IF NOT EXISTS AlertDetails (
    AlertID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Message TEXT NOT NULL,
    SentTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PostedBy INTEGER NOT NULL,
    PostedByRole VARCHAR(20),
    UrgencyLevel INTEGER CHECK (UrgencyLevel BETWEEN 1 AND 5),
    Protocol TEXT,
    INDEX idx_alert_senttime (SentTime),
    INDEX idx_alert_urgency (UrgencyLevel),
    INDEX idx_alert_postedby (PostedBy, PostedByRole)
);

CREATE TABLE IF NOT EXISTS AlertsDoctors (
    AlertID INTEGER,
    DoctorID INTEGER,
    AcknowledgedTime DATETIME DEFAULT NULL,
    PRIMARY KEY (AlertID, DoctorID),
    FOREIGN KEY (AlertID) REFERENCES AlertDetails(AlertID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID) ON DELETE CASCADE,
    INDEX idx_alert_doctor (DoctorID),
    INDEX idx_alert_doctor_ack (AcknowledgedTime)
);

CREATE TABLE IF NOT EXISTS AlertsNurse (
    AlertID INTEGER,
    NurseID INTEGER,
    AcknowledgedTime DATETIME DEFAULT NULL,
    PRIMARY KEY (AlertID, NurseID),
    FOREIGN KEY (AlertID) REFERENCES AlertDetails(AlertID) ON DELETE CASCADE,
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE,
    INDEX idx_alert_nurse (NurseID),
    INDEX idx_alert_nurse_ack (AcknowledgedTime)
);

INSERT INTO Doctor (FirstName, LastName, Specialty, YearOfExperience) VALUES
('Maya', 'Ellison', 'Cardiology', 15),
('Michael', 'Chen', 'Internal Medicine', 12),
('Emily', 'Rodriguez', 'Pediatrics', 8),
('James', 'Williams', 'Emergency Medicine', 20),
('Lisa', 'Anderson', 'Neurology', 10),
('Robert', 'Martinez', 'Orthopedics', 18),
('Jennifer', 'Davis', 'Oncology', 14),
('David', 'Brown', 'Psychiatry', 7),
('Maria', 'Garcia', 'Dermatology', 9),
('Thomas', 'Wilson', 'General Surgery', 22);

INSERT INTO Nurse (FirstName, LastName) VALUES
('Nic', 'Nevin'),
('John', 'Miller'),
('Patricia', 'Jones'),
('Kevin', 'Taylor'),
('Susan', 'Moore'),
('Brian', 'Jackson'),
('Nancy', 'White'),
('Christopher', 'Harris'),
('Linda', 'Martin'),
('Daniel', 'Clark');

INSERT INTO Insurance (InsuranceProvider, PolicyNumber, Deductible, DueDate) VALUES
('Blue Cross Blue Shield', 'BCBS-2024-001', 500.00, '2024-12-31'),
('United Healthcare', 'UHC-2024-002', 750.00, '2024-11-30'),
('Aetna', 'AET-2024-003', 1000.00, '2024-10-31'),
('Cigna', 'CIG-2024-004', 600.00, '2024-09-30'),
('Humana', 'HUM-2024-005', 850.00, '2024-08-31'),
('Kaiser Permanente', 'KP-2024-006', 400.00, '2024-07-31'),
('Anthem', 'ANT-2024-007', 900.00, '2024-06-30'),
('Medicare', 'MED-2024-008', 200.00, '2024-05-31'),
('Medicaid', 'MCD-2024-009', 0.00, '2024-04-30'),
('MetLife', 'MET-2024-010', 1200.00, '2024-03-31'),
('Blue Cross Blue Shield', 'BCBS-2024-011', 650.00, '2024-02-29'),
('United Healthcare', 'UHC-2024-012', 800.00, '2024-01-31'),
('Aetna', 'AET-2024-013', 1100.00, '2024-12-15'),
('Cigna', 'CIG-2024-014', 700.00, '2024-11-15'),
('Humana', 'HUM-2024-015', 950.00, '2024-10-15'),
('Blue Cross Blue Shield', 'BCBS-2024-016', 550.00, '2024-09-15'),
('United Healthcare', 'UHC-2024-017', 900.00, '2024-08-15'),
('Aetna', 'AET-2024-018', 1200.00, '2024-07-15');

INSERT INTO Visits (AdmitReason, AppointmentDate, NextVisitDate) VALUES
('Annual physical examination', '2024-01-15', '2025-01-15'),
('Chest pain and shortness of breath', '2024-02-20', '2024-03-20'),
('Pediatric wellness check', '2024-03-10', '2024-09-10'),
('Emergency - fractured ankle', '2024-03-25', '2024-04-08'),
('Migraine headaches', '2024-04-05', '2024-05-05'),
('Knee replacement surgery consultation', '2024-04-18', '2024-05-02'),
('Chemotherapy treatment', '2024-05-01', '2024-05-15'),
('Depression and anxiety evaluation', '2024-05-10', '2024-05-24'),
('Severe acne treatment', '2024-05-20', '2024-06-20'),
('Appendectomy', '2024-06-01', '2024-06-15'),
('Diabetes management', '2024-06-10', '2024-09-10'),
('Hypertension follow-up', '2024-06-15', '2024-08-15'),
('Pregnancy checkup', '2024-06-20', '2024-07-04'),
('Allergic reaction', '2024-06-25', NULL),
('COVID-19 symptoms', '2024-07-01', '2024-07-15');

INSERT INTO VitalChart (HeartRate, BloodPressure, RespiratoryRate, Temperature) VALUES
(72, '120/80', 16, 98.6),
(95, '145/95', 20, 99.1),
(85, '110/70', 18, 98.4),
(88, '130/85', 22, 99.8),
(78, '125/82', 17, 98.7),
(70, '118/78', 15, 98.5),
(82, '135/88', 19, 99.0),
(76, '122/80', 16, 98.6),
(68, '115/75', 14, 98.3),
(90, '140/90', 21, 100.2),
(74, '128/84', 17, 98.8),
(92, '150/95', 20, 99.5),
(80, '125/80', 18, 98.6),
(100, '138/92', 24, 101.0),
(86, '132/86', 19, 99.2);

INSERT INTO `Condition` (Description, Treatment) VALUES
('Healthy - no significant findings', 'Continue regular checkups'),
('Angina pectoris', 'Nitroglycerin, beta blockers, lifestyle modifications'),
('Normal pediatric development', 'Continue routine vaccinations'),
('Fractured lateral malleolus', 'Cast immobilization for 6 weeks, physical therapy'),
('Concussion', 'Rest, avoid further head trauma'),
('Severe osteoarthritis of knee', 'Total knee replacement recommended'),
('Stage II breast cancer', 'Chemotherapy, radiation therapy'),
('Major depressive disorder', 'Antidepressants, cognitive behavioral therapy'),
('Cystic acne', 'Isotretinoin treatment, topical retinoids'),
('Acute appendicitis', 'Laparoscopic appendectomy performed'),
('Type 2 diabetes mellitus', 'Metformin, diet control, exercise'),
('Essential hypertension', 'ACE inhibitors, low sodium diet'),
('Normal pregnancy - 20 weeks', 'Prenatal vitamins, regular monitoring'),
('Anaphylactic reaction', 'Epinephrine, antihistamines, observation'),
('COVID-19 infection - mild', 'Rest, isolation, symptomatic treatment');

INSERT INTO Discharge (DischargeDate, Instructions) VALUES
('2024-01-15', 'Continue healthy lifestyle. Schedule next annual exam.'),
('2024-02-21', 'Take medications as prescribed. Follow up with cardiologist in 1 month.'),
('2024-03-10', 'Continue regular feeding schedule. Return for 9-month checkup.'),
('2024-03-26', 'Keep cast dry. Use crutches. Return in 2 weeks for X-ray.'),
('2024-04-05', 'Take preventive medication daily. Keep headache diary.'),
('2024-04-18', 'Schedule surgery. Begin pre-operative exercises.'),
('2024-05-01', 'Rest between treatments. Monitor for side effects.'),
('2024-05-10', 'Take medication as prescribed. Continue therapy sessions.'),
('2024-05-20', 'Apply medication as directed. Avoid sun exposure.'),
('2024-06-04', 'Rest for 2 weeks. No heavy lifting for 6 weeks.'),
('2024-06-10', 'Monitor blood sugar daily. Follow diabetic diet plan.'),
('2024-06-15', 'Take blood pressure medication daily. Reduce salt intake.'),
('2024-06-20', 'Continue prenatal vitamins. Avoid heavy lifting.'),
('2024-06-25', 'Carry EpiPen. Avoid known allergens. Follow up with allergist.'),
('2024-07-01', 'Isolate for 5 days. Rest and hydrate. Return if symptoms worsen.');

INSERT INTO Patient (FirstName, LastName, DOB, Weight, BloodType, PreExisting, InsuranceID, DischargeID, ConditionID, DoctorID, NurseID, VitalID, VisitID) VALUES
('Joe', 'Pesci', '1980-05-15', 145.5, 'O+', FALSE, 11, 10, 5, 2, 1, 1, 5),
('Bob', 'Johnson', '1955-08-22', 182.0, 'A+', TRUE, 12, 2, 2, 1, 2, 2, 2),
('Charlie', 'Williams', '2018-12-10', 42.5, 'B+', FALSE, 3, 3, 3, 3, 3, 3, 3),
('Diana', 'Brown', '1992-03-18', 130.0, 'AB+', FALSE, 13, 4, 4, 6, 4, 4, 4),
('Edward', 'Davis', '1975-11-30', 195.5, 'O-', TRUE, 14, 5, 5, 5, 5, 5, 5),
('Fiona', 'Miller', '1948-07-05', 168.0, 'A-', TRUE, 6, 6, 6, 6, 6, 6, 6),
('George', 'Wilson', '1960-09-12', 210.0, 'B-', TRUE, 7, 7, 7, 7, 7, 7, 7),
('Hannah', 'Moore', '1995-01-25', 125.5, 'AB-', TRUE, 8, 8, 8, 8, 8, 8, 8),
('Ian', 'Taylor', '2000-06-08', 155.0, 'O+', FALSE, 15, 9, 9, 9, 9, 9, 9),
('Julia', 'Anderson', '1988-04-20', 138.5, 'A+', FALSE, 16, 10, 10, 10, 10, 10, 10),
('Kevin', 'Thomas', '1970-02-14', 220.0, 'B+', TRUE, 1, 11, 11, 2, 1, 11, 11),
('Laura', 'Jackson', '1965-10-28', 160.0, 'O-', TRUE, 2, 12, 12, 1, 2, 12, 12),
('Mike', 'White', '1990-12-03', 175.5, 'A-', FALSE, 3, 13, 13, 3, 3, 13, 13),
('Nina', 'Harris', '1985-08-17', 142.0, 'AB+', TRUE, 4, 14, 14, 4, 4, 14, 14),
('Oliver', 'Martin', '1978-05-22', 188.0, 'B-', FALSE, 5, 15, 15, 2, 5, 15, 15);

INSERT INTO Proxy (PatientID, FirstName, LastName, Relationship) VALUES
(1, 'Nina', 'Pesci', 'Daughter'),
(3, 'John', 'Williams', 'Father'),
(6, 'Robert', 'Miller', 'Son'),
(7, 'Lisa', 'Wilson', 'Daughter'),
(8, 'Mark', 'Moore', 'Spouse'),
(4, 'Ryan', 'Moochi', 'Daughter'),
(2, 'Thomas', 'Jefferson', 'spouse'),
(4, 'Nina', 'Pesci', 'Sister'),
(5, 'Micheal', 'Jord', 'Brother'),
(9, 'Willow', 'Hindon', 'Aunt'),
(10, 'Arthur', 'Morely', 'Son');

INSERT INTO Medication (PrescriptionName, DosageAmount, DosageUnit, PickUpLocation, RefillsLeft, FrequencyAmount, FrequencyPeriod) VALUES
('Lisinopril', 10, 'mg', 'CVS Pharmacy - Main St', 5, 1, 'daily'),
('Metformin', 500, 'mg', 'Walgreens - Oak Ave', 3, 2, 'daily'),
('Atorvastatin', 20, 'mg', 'Hospital Pharmacy', 6, 1, 'daily'),
('Amoxicillin', 500, 'mg', 'CVS Pharmacy - Main St', 0, 3, 'daily'),
('Ibuprofen', 400, 'mg', 'Rite Aid - Center Blvd', 2, 3, 'daily'),
('Sertraline', 50, 'mg', 'Walgreens - Oak Ave', 4, 1, 'daily'),
('Omeprazole', 20, 'mg', 'Hospital Pharmacy', 5, 1, 'daily'),
('Levothyroxine', 75, 'mcg', 'CVS Pharmacy - Main St', 6, 1, 'daily'),
('Albuterol', 90, 'mcg', 'Walgreens - Oak Ave', 1, 2, 'as needed'),
('Prednisone', 10, 'mg', 'Hospital Pharmacy', 0, 1, 'daily'),
('Metoprolol', 25, 'mg', 'CVS Pharmacy - Main St', 3, 2, 'daily'),
('Gabapentin', 300, 'mg', 'Rite Aid - Center Blvd', 4, 3, 'daily'),
('Insulin Glargine', 10, 'units', 'Hospital Pharmacy', 5, 1, 'daily'),
('Aspirin', 81, 'mg', 'Walgreens - Oak Ave', 6, 1, 'daily'),
('Acetaminophen', 500, 'mg', 'CVS Pharmacy - Main St', 2, 4, 'daily'),
('Warfarin', 5, 'mg', 'Hospital Pharmacy', 8, 1, 'daily'),
('Furosemide', 40, 'mg', 'CVS Pharmacy - Main St', 4, 2, 'daily'),
('Lorazepam', 1, 'mg', 'Walgreens - Oak Ave', 3, 1, 'as needed');

INSERT INTO Patient_Medications (PatientID, MedicationID, PrescribedDate, EndDate) VALUES
(2, 1, '2024-02-20', '2025-02-20'),
(2, 3, '2024-02-20', '2025-02-20'),
(2, 14, '2024-02-20', NULL),
(4, 5, '2024-03-25', '2024-04-25'),
(5, 12, '2024-04-05', NULL),
(6, 5, '2024-04-18', '2024-05-18'),
(7, 10, '2024-05-01', '2024-05-15'),
(8, 6, '2024-05-10', NULL),
(9, 4, '2024-05-20', '2024-05-30'),
(10, 4, '2024-06-01', '2024-06-11'),
(10, 15, '2024-06-01', '2024-06-15'),
(11, 2, '2024-06-10', NULL),
(11, 13, '2024-06-10', NULL),
(12, 1, '2024-06-15', NULL),
(12, 11, '2024-06-15', NULL),
(14, 10, '2024-06-25', '2024-06-30'),
(15, 15, '2024-07-01', '2024-07-08'),
(1, 16, '2024-07-15', NULL),
(3, 17, '2024-07-20', NULL),
(4, 18, '2024-07-25', NULL);

INSERT INTO MessageDetails (Subject, Content, PostedBy, PostedByRole, SenderType, ReadStatus, Priority) VALUES
('Lab Results Ready', 'Your lab results are ready. Everything looks normal.', 2, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Follow-up Appointment', 'Please schedule your follow-up appointment for next month.', 1, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Medication Reminder', 'Remember to take your medication with food.', 3, 'Doctor', 'Doctor', FALSE, 'Normal'),
('X-ray Progress', 'Your X-ray shows good healing progress.', 6, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Medication Effectiveness', 'How are you feeling with the new medication?', 5, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Surgery Schedule', 'Surgery scheduled for May 15th at 8 AM.', 6, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Chemotherapy Appointment', 'Please arrive 30 minutes before your chemotherapy appointment.', 7, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Prescription Sent', 'Your prescription has been sent to the pharmacy.', 8, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Medication Warning', 'Avoid direct sunlight while on this medication.', 9, 'Doctor', 'Doctor', FALSE, 'High'),
('Post-surgery Recovery', 'Post-surgery recovery is going well. Continue rest.', 10, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Cardiology Consultation', 'Cardiology consultation scheduled for next week.', 1, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Internal Medicine Follow-up', 'Internal medicine follow-up required.', 2, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Vaccination Records', 'Pediatric vaccination records updated.', 3, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Emergency Protocol', 'Emergency department protocol review needed.', 4, 'Nurse', 'Nurse', FALSE, 'High'),
('Neurology Consultation', 'Neurology consultation results available.', 5, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Orthopedic Preparation', 'Orthopedic surgery preparation instructions.', 6, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Oncology Treatment', 'Oncology treatment plan updated.', 7, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Psychiatry Session', 'Psychiatry session notes completed.', 8, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Dermatology Biopsy', 'Dermatology biopsy results ready.', 9, 'Nurse', 'Nurse', FALSE, 'Normal'),
('General Surgery Pre-op', 'General surgery pre-op instructions sent.', 10, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Patient Transfer', 'Patient transfer to ICU completed.', 1, 'Doctor', 'Doctor', FALSE, 'High'),
('Medication Reconciliation', 'Medication reconciliation completed.', 2, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Discharge Planning', 'Discharge planning meeting scheduled.', 3, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Family Consultation', 'Family consultation requested.', 4, 'Doctor', 'Doctor', FALSE, 'High'),
('Lab Work', 'Lab work ordered for tomorrow.', 5, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Physical Therapy', 'Physical therapy evaluation completed.', 6, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Chemotherapy Side Effects', 'Chemotherapy side effects documented.', 7, 'Doctor', 'Doctor', FALSE, 'High'),
('Mental Health Assessment', 'Mental health assessment completed.', 8, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Skin Condition', 'Skin condition improved with treatment.', 9, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Surgical Site', 'Surgical site healing well.', 10, 'Doctor', 'Doctor', FALSE, 'Normal'),
('Morning Rounds', 'Morning rounds completed for all patients.', 1, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Medication Administration', 'Medication administration completed.', 2, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Vital Signs', 'Vital signs recorded for all patients.', 3, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Patient Comfort', 'Patient comfort measures implemented.', 4, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Care Plan Updates', 'Care plan updates completed.', 5, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Equipment Maintenance', 'Equipment maintenance scheduled.', 6, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Patient Education', 'Patient education materials distributed.', 7, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Safety Protocols', 'Safety protocols reviewed with team.', 8, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Infection Control', 'Infection control measures implemented.', 9, 'Nurse', 'Nurse', FALSE, 'Normal'),
('Emergency Response', 'Emergency response drill completed.', 10, 'Nurse', 'Nurse', FALSE, 'High');

INSERT INTO MessagePatients (MessageID, PatientID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15);

INSERT INTO MessageDoctor (MessageID, DoctorID) VALUES
(2, 1),
(11, 1),
(20, 1),
(1, 2),
(12, 2),
(21, 2),
(3, 3),
(13, 3),
(22, 3),
(4, 4),
(14, 4),
(23, 4),
(5, 5),
(15, 5),
(24, 5),
(6, 6),
(16, 6),
(25, 6),
(7, 7),
(17, 7),
(26, 7),
(8, 8),
(18, 8),
(27, 8),
(9, 9),
(19, 9),
(28, 9),
(10, 10),
(20, 10),
(29, 10);

INSERT INTO MessageNurse (MessageID, NurseID) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 2),
(5, 2),
(6, 2),
(7, 3),
(8, 3),
(9, 3),
(10, 4),
(11, 4),
(12, 4),
(13, 5),
(14, 5),
(15, 5),
(16, 6),
(17, 6),
(18, 6),
(19, 7),
(20, 7),
(21, 7),
(22, 8),
(23, 8),
(24, 8),
(25, 9),
(26, 9),
(27, 9),
(28, 10),
(29, 10),
(30, 10);

INSERT INTO AlertDetails (Message, PostedBy, PostedByRole, UrgencyLevel, Protocol) VALUES
('Patient blood pressure critically high: 180/110', 2, 'Nurse', 5, 'Immediate intervention required. Administer antihypertensive medication.'),
('Allergic reaction detected - patient requires immediate attention', 4, 'Nurse', 5, 'Administer epinephrine immediately. Monitor airway.'),
('Post-surgery temperature elevated: 101.5F', 10, 'Nurse', 3, 'Monitor closely. Administer antipyretics if temperature exceeds 102F.'),
('Patient missed scheduled chemotherapy appointment', 7, 'Nurse', 2, 'Contact patient to reschedule. Document reason for absence.'),
('Abnormal lab results: Glucose level 450 mg/dL', 1, 'Nurse', 4, 'Check for ketones. Consider insulin adjustment. Notify endocrinologist.'),
('Patient fall reported in room 205', 4, 'Nurse', 4, 'Assess for injuries. Complete incident report. Order imaging if needed.'),
('Medication interaction warning: Warfarin and Aspirin', 2, 'System', 3, 'Review dosages. Monitor INR closely. Consider alternative therapy.'),
('Critical potassium level: 2.8 mEq/L', 5, 'Nurse', 4, 'Administer potassium supplement. Continuous cardiac monitoring required.');

INSERT INTO AlertsDoctors (AlertID, DoctorID, AcknowledgedTime) VALUES
(1, 1, '2024-02-20 15:35:00'),
(2, 4, '2024-06-25 14:02:00'),
(3, 10, '2024-06-02 22:10:00'),
(4, 7, '2024-05-15 09:30:00'),
(5, 2, '2024-06-10 08:00:00'),
(6, 6, '2024-04-08 03:30:00'),
(7, 1, '2024-02-20 10:15:00'),
(8, 2, '2024-07-01 06:45:00');

INSERT INTO AlertsNurse (AlertID, NurseID, AcknowledgedTime) VALUES
(1, 2, '2024-02-20 15:31:00'),
(2, 4, '2024-06-25 14:01:00'),
(3, 10, '2024-06-02 22:02:00'),
(4, 7, '2024-05-15 09:05:00'),
(5, 1, '2024-06-10 07:50:00'),
(6, 4, '2024-04-08 03:17:00'),
(7, 2, '2024-02-20 10:02:00'),
(8, 5, '2024-07-01 06:32:00');