# VitalFlow API

## Base URL

```
http://localhost:4001
```

## Endpoints

### Patients

- `GET /patient/` - Get all patients
- `GET /patient/{id}` - Get patient by ID
- `GET /patient/{id}/vitals` - Get patient vitals
- `GET /patient/{id}/medications` - Get patient medications
- `GET /patient/{id}/condition` - Get patient condition
- `GET /patient/{id}/doctor` - Get patient's doctor
- `GET /patient/{id}/nurse` - Get patient's nurse
- `GET /patient/{id}/proxy` - Get patient's proxy
- `GET /patient/{id}/insurance` - Get patient's insurance
- `GET /patient/{id}/discharge` - Get patient's discharge info

### Visits

- `GET /visit/` - Get all visits
- `GET /visit/{id}` - Get visit by ID
- `POST /visit/` - Create new visit
- `PUT /visit/{id}` - Update visit

### Vitals

- `GET /vital/` - Get all vital charts
- `GET /vital/{id}` - Get vital chart by ID
- `POST /vital/` - Create new vital chart

### Conditions

- `GET /condition/` - Get all conditions
- `GET /condition/{id}` - Get condition by ID
- `POST /condition/` - Create new condition
- `PUT /condition/{id}` - Update condition

### Medications

- `GET /medication/` - Get all medications
- `GET /medication/{id}` - Get medication by ID
- `GET /medication/patient_medications` - Get patient-medication links
- `POST /medication/patient_medications` - Link patient to medication

### Discharges

- `GET /discharge/` - Get all discharges
- `GET /discharge/{id}` - Get discharge by ID
- `POST /discharge/` - Create new discharge

### Insurance

- `GET /insurance/` - Get all insurance
- `GET /insurance/{id}` - Get insurance by ID

### Staff

- `GET /doctor/` - Get all doctors
- `GET /doctor/{id}` - Get doctor by ID
- `GET /nurse/` - Get all nurses
- `GET /nurse/{id}` - Get nurse by ID

### Proxies

- `GET /proxy/` - Get all proxies
- `GET /proxy/{id}` - Get proxy by ID
- `GET /proxy/{id}/patients` - Get patients by proxy

### Messages

- `GET /message/?user_type={type}&user_id={id}` - Get messages for user
- `POST /message/` - Create message
- `GET /message/{id}` - Get message by ID

### Alerts

- `GET /alert/?user_type={type}&user_id={id}` - Get alerts for user
- `POST /alert/` - Create alert
- `GET /alert/{id}` - Get alert by ID
- `PUT /alert/{id}` - Acknowledge alert

## Data Examples

### Patient

```json
{
  "PatientID": 1,
  "FirstName": "Alice",
  "LastName": "Smith",
  "DOB": "Thu, 15 May 1980 00:00:00 GMT",
  "BloodType": "O+",
  "Weight": "145.50"
}
```

### Doctor

```json
{
  "DoctorID": 1,
  "FirstName": "Sarah",
  "LastName": "Johnson",
  "Specialty": "Cardiology",
  "YearOfExperience": 15
}
```

## Usage

Use Curl or postman

### Get patient medications

```bash
curl "http://localhost:4001/patient/2/medications"
```

### Create visit

```bash
curl -X POST "http://localhost:4000/visit/" \
  -H "Content-Type: application/json" \
  -d '{"AdmitReason": "Checkup", "AppointmentDate": "2024-08-15"}'
```

### Get messages for patient

```bash
curl "http://localhost:4000/message/?user_type=patient&user_id=1"
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

## Test

1. Start Docker: `docker compose -f sandbox.yaml up -d`
2. API: `http://localhost:4000`
3. App: `http://localhost:8501`
