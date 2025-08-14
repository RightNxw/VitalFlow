# VitalFlow API

## Base URL

```
http://localhost:4000
```

## Overview

The VitalFlow API is a comprehensive healthcare management system that provides endpoints for managing patients, doctors, nurses, proxies, visits, vitals, conditions, medications, discharges, insurance, messages, and alerts. The API follows RESTful principles and uses MySQL as the backend database.

## Authentication & Authorization

The API implements role-based access control with the following user types:
- **Doctor**: Full access to patient data, vitals, conditions, and medical records
- **Nurse**: Access to patient vitals, basic patient info, and care coordination
- **Patient**: Access to own medical records, medications, and appointments
- **Proxy**: Access to dependent patient information and care coordination

## Endpoints

### Patients 

- `GET /patient/` - Get all patients
- `GET /patient/<int:patient_id>` - Get patient by ID
- `PUT /patient/<int:patient_id>` - Update patient information (DischargeID, ConditionID, DoctorID, NurseID, VitalID, VisitID)
- `GET /patient/<int:patient_id>/medications` - Get patient medications
- `GET /patient/<int:patient_id>/vitals` - Get patient vitals
- `GET /patient/<int:patient_id>/condition` - Get patient condition
- `GET /patient/<int:patient_id>/discharge` - Get patient discharge info
- `GET /patient/<int:patient_id>/doctor` - Get patient's doctor
- `GET /patient/<int:patient_id>/nurse` - Get patient's nurse
- `GET /patient/<int:patient_id>/insurance` - Get patient's insurance
- `GET /patient/<int:patient_id>/proxy` - Get patient's proxy
- `GET /patient/<int:patient_id>/visit` - Get patient's current visit

### Doctors 

- `GET /doctor/` - Get all doctors
- `GET /doctor/<int:doctor_id>` - Get doctor by ID

### Nurses 

- `GET /nurse/` - Get all nurses
- `GET /nurse/<int:nurse_id>` - Get nurse by ID

### Proxies 

- `GET /proxy/` - Get all proxies
- `GET /proxy/<int:proxy_id>` - Get proxy by ID
- `GET /proxy/name/<string:first_name>/<string:last_name>` - Get proxy by name
- `GET /proxy/<int:proxy_id>/patients` - Get patients for a specific proxy

### Visits 

- `GET /visit/` - Get all visits
- `GET /visit/<int:visit_id>` - Get visit by ID
- `POST /visit/` - Create new visit
- `PUT /visit/<int:visit_id>` - Update visit

### Vitals

- `GET /vital/` - Get all vital charts
- `GET /vital/<int:vital_id>` - Get vital chart by ID
- `POST /vital/` - Create new vital chart

### Conditions 

- `GET /condition/` - Get all conditions
- `GET /condition/<int:condition_id>` - Get condition by ID
- `POST /condition/` - Create new condition
- `PUT /condition/<int:condition_id>` - Update condition

### Medications 

- `GET /medication/` - Get all medications
- `GET /medication/<int:medication_id>` - Get medication by ID
- `GET /medication/patient_medications` - Get patient-medication links
- `POST /medication/patient_medications` - Link patient to medication

### Discharges

- `GET /discharge/` - Get all discharges
- `GET /discharge/<int:discharge_id>` - Get discharge by ID
- `POST /discharge/` - Create new discharge

### Insurance 

- `GET /insurance/` - Get all insurance
- `GET /insurance/<int:insurance_id>` - Get insurance by ID

### Messages

- `GET /message/?user_type={type}&user_id={id}` - Get messages for user (patient, doctor, or nurse)
- `POST /message/` - Create new message
- `GET /message/<int:message_id>` - Get message by ID
- `PUT /message/<int:message_id>` - Update message
- `DELETE /message/<int:message_id>` - Delete message

### Alerts 

- `GET /alert/?user_type={type}&user_id={id}` - Get alerts for user
- `POST /alert/` - Create new alert
- `GET /alert/<int:alert_id>` - Get alert by ID
- `PUT /alert/<int:alert_id>` - Update alert
- `DELETE /alert/<int:alert_id>` - Delete alert

## Data Models

### Patient

```json
{
  "PatientID": 1,
  "FirstName": "Joe",
  "LastName": "Pesci",
  "DOB": "1980-05-15",
  "Weight": 145.5,
  "BloodType": "O+",
  "PreExisting": false,
  "InsuranceID": 11,
  "DischargeID": 10,
  "ConditionID": 5,
  "DoctorID": 2,
  "NurseID": 1,
  "VitalID": 1,
  "VisitID": 5
}
```

### Doctor

```json
{
  "DoctorID": 1,
  "FirstName": "Maya",
  "LastName": "Ellison",
  "Specialty": "Cardiology",
  "YearOfExperience": 15
}
```

### Nurse

```json
{
  "NurseID": 1,
  "FirstName": "Nic",
  "LastName": "Nevin"
}
```

### Proxy

```json
{
  "ProxyID": 1,
  "PatientID": 1,
  "FirstName": "Nina",
  "LastName": "Pesci",
  "Relationship": "Daughter"
}
```

### Visit

```json
{
  "VisitID": 1,
  "AdmitReason": "Chest pain and shortness of breath",
  "AppointmentDate": "2024-02-20",
  "NextVisitDate": "2024-03-20"
}
```

### Vital Chart

```json
{
  "VitalID": 1,
  "HeartRate": 72,
  "BloodPressure": "120/80",
  "RespiratoryRate": 16,
  "Temperature": 98.6
}
```

### Condition

```json
{
  "ConditionID": 1,
  "Description": "Healthy - no significant findings",
  "Treatment": "Continue regular checkups"
}
```

### Medication

```json
{
  "MedicationID": 1,
  "PrescriptionName": "Lisinopril",
  "DosageAmount": 10.0,
  "DosageUnit": "mg",
  "PickUpLocation": "CVS Pharmacy - Main St",
  "RefillsLeft": 5,
  "FrequencyAmount": 1,
  "FrequencyPeriod": "daily"
}
```

### Patient Medication Link

```json
{
  "PatientID": 2,
  "MedicationID": 1,
  "PrescribedDate": "2024-02-20",
  "EndDate": "2025-02-20"
}
```

### Discharge

```json
{
  "DischargeID": 1,
  "DischargeDate": "2024-01-15",
  "Instructions": "Continue healthy lifestyle. Schedule next annual exam."
}
```

### Insurance

```json
{
  "InsuranceID": 1,
  "InsuranceProvider": "Blue Cross Blue Shield",
  "PolicyNumber": "BCBS-2024-001",
  "Deductible": 500.00,
  "DueDate": "2024-12-31"
}
```

### Message

```json
{
  "MessageID": 1,
  "Subject": "Lab Results Ready",
  "Content": "Your lab results are ready. Everything looks normal.",
  "SentTime": "2024-08-18T10:00:00",
  "PostedBy": 2,
  "PostedByRole": "Doctor",
  "SenderType": "Doctor",
  "ReadStatus": false,
  "Priority": "Normal"
}
```

### Alert

```json
{
  "AlertID": 1,
  "Message": "Patient blood pressure critically high: 180/110",
  "SentTime": "2024-08-15T10:30:00",
  "PostedBy": 2,
  "PostedByRole": "Nurse",
  "UrgencyLevel": 5,
  "Protocol": "Immediate intervention required. Administer antihypertensive medication."
}
```

## Usage Examples

### Get all patients

```bash
curl "http://localhost:4000/patient/"
```

### Get patient medications

```bash
curl "http://localhost:4000/patient/2/medications"
```

### Create new visit

```bash
curl -X POST "http://localhost:4000/visit/" \
  -H "Content-Type: application/json" \
  -d '{"AdmitReason": "Annual checkup", "AppointmentDate": "2024-08-15"}'
```

### Get messages for a doctor

```bash
curl "http://localhost:4000/message/?user_type=doctor&user_id=1"
```

### Create new vital chart

```bash
curl -X POST "http://localhost:4000/vital/" \
  -H "Content-Type: application/json" \
  -d '{"HeartRate": 75, "BloodPressure": "120/80", "RespiratoryRate": 16, "Temperature": 98.6}'
```

### Get proxy's patients

```bash
curl "http://localhost:4000/proxy/1/patients"
```

## HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (missing required fields, invalid data)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error (database errors, server issues)

## Error Response Format

```json
{
  "error": "Error message description"
}
```

## Database Schema

The API connects to a MySQL database with the following key tables:
- **Patient** - Core patient information and relationships
- **Doctor** - Physician information and specialties
- **Nurse** - Nursing staff information
- **Proxy** - Patient representatives and guardians
- **Visits** - Patient appointments and encounters
- **VitalChart** - Patient vital signs and measurements
- **Condition** - Medical conditions and treatments
- **Medication** - Prescription medications
- **Patient_Medications** - Patient-medication relationships
- **Discharge** - Patient discharge information
- **Insurance** - Insurance coverage details
- **MessageDetails** - Communication messages
- **AlertDetails** - Clinical alerts and notifications

## Development & Testing

### Local Development

1. Start Docker containers: `docker compose -f sandbox.yaml up -d`
2. API will be available at: `http://localhost:4000`
3. Streamlit app will be available at: `http://localhost:8501`
4. Database will be available at: `localhost:3306`

### API Testing

- Use tools like Postman, Insomnia, or curl for testing endpoints
- All endpoints return JSON responses
- POST/PUT requests require `Content-Type: application/json` header
- Check the logs directory for detailed API request/response logging

### Database Connection

The API automatically connects to the MySQL database using environment variables:
- `DB_USER` - Database username
- `MYSQL_ROOT_PASSWORD` - Database password
- `DB_HOST` - Database host (default: db)
- `DB_PORT` - Database port (default: 3306)
- `DB_NAME` - Database name (default: vitalflow_database)

## Security Notes

- Input validation is performed on all POST/PUT requests
- Role-based access control is implemented at the application level upon 'login' per persona
