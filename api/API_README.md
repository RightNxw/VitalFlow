# VitalFlow API

## Base URL

```
http://localhost:4001
```

## Endpoints

### Patients

- `GET /patient/patients` - Get all patients
- `GET /patient/patients/{id}` - Get patient by ID
- `GET /patient/patients/{id}/vitals` - Get patient vitals
- `GET /patient/patients/{id}/medications` - Get patient medications
- `GET /patient/patients/{id}/condition` - Get patient condition
- `GET /patient/patients/{id}/doctor` - Get patient's doctor
- `GET /patient/patients/{id}/nurse` - Get patient's nurse
- `GET /patient/patients/{id}/proxy` - Get patient's proxy
- `GET /patient/patients/{id}/insurance` - Get patient's insurance
- `GET /patient/patients/{id}/discharge` - Get patient's discharge info

### Visits

- `GET /visit/visits` - Get all visits
- `GET /visit/visits/{id}` - Get visit by ID
- `POST /visit/visits` - Create new visit
- `PUT /visit/visits/{id}` - Update visit

### Vitals

- `GET /vital/vitalcharts` - Get all vital charts
- `GET /vital/vitalcharts/{id}` - Get vital chart by ID
- `POST /vital/vitalcharts` - Create new vital chart

### Conditions

- `GET /condition/conditions` - Get all conditions
- `GET /condition/conditions/{id}` - Get condition by ID
- `POST /condition/conditions` - Create new condition
- `PUT /condition/conditions/{id}` - Update condition

### Medications

- `GET /medication/medications` - Get all medications
- `GET /medication/medications/{id}` - Get medication by ID
- `GET /medication/patient_medications` - Get patient-medication links
- `POST /medication/patient_medications` - Link patient to medication

### Discharges

- `GET /discharge/discharge` - Get all discharges
- `GET /discharge/discharge/{id}` - Get discharge by ID
- `POST /discharge/discharge` - Create new discharge

### Insurance

- `GET /insurance/insurance` - Get all insurance
- `GET /insurance/insurance/{id}` - Get insurance by ID

### Staff

- `GET /doctors` - Get all doctors
- `GET /doctors/{id}` - Get doctor by ID
- `GET /nurses` - Get all nurses
- `GET /nurses/{id}` - Get nurse by ID

### Proxies

- `GET /proxies` - Get all proxies
- `GET /proxies/{id}` - Get proxy by ID
- `GET /proxies/{id}/patients` - Get patients by proxy

### Messages

- `GET /messages?user_type={type}&user_id={id}` - Get messages for user
- `POST /messages` - Create message
- `GET /messages/{id}` - Get message by ID

### Alerts

- `GET /alerts?user_type={type}&user_id={id}` - Get alerts for user
- `POST /alerts` - Create alert
- `GET /alerts/{id}` - Get alert by ID
- `PUT /alerts/{id}` - Acknowledge alert

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
curl "http://localhost:4001/patient/patients/2/medications"
```

### Create visit

```bash
curl -X POST "http://localhost:4001/visit/visits" \
  -H "Content-Type: application/json" \
  -d '{"AdmitReason": "Checkup", "AppointmentDate": "2024-08-15"}'
```

### Get messages for patient

```bash
curl "http://localhost:4001/messages?user_type=patient&user_id=1"
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

## Test

1. Start Docker: `docker compose -f sandbox.yaml up -d`
2. API: `http://localhost:4001`
3. App: `http://localhost:8502`
