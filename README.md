# VitalFlow - Healthcare Portal

A comprehensive healthcare management system built with Streamlit frontend and Flask API backend, designed to streamline patient care, billing, and communication between healthcare providers and patients.

## Features

### **Multi-Persona Access**

- **Doctor Portal** - Patient management, medical charts, alerts, and communications
- **Nurse Portal** - Patient care, vitals monitoring, and care coordination
- **Proxy Portal** - Manage dependent patients, insurance, and billing
- **Patient Portal** - Personal health records, medications, and appointments

### **Core Functionality**

- **Patient Management** - Comprehensive patient records and medical history
- **Insurance & Billing** - Policy management and deductible tracking
- **Communication System** - Secure messaging between healthcare teams
- **Medical Records** - Vitals, conditions, medications, and visit tracking
- **Alert System** - Medical alerts and notifications
- **Dashboard Analytics** - Real-time metrics and insights

## Quick Start

### **Prerequisites**

- Docker and Docker Compose
- Python 3.8+
- MySQL database

### **Installation**

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/VitalFlow.git
   cd VitalFlow
   ```

2. **Start the application**

   ```bash
   # Start all services
   docker-compose up -d

   # Or use sandbox configuration for testing
   docker-compose -f sandbox.yaml up -d
   ```

3. **Access the application**
   - **Frontend**: http://localhost:8501
   - **API**: http://localhost:4000
   - **Database**: localhost:3306

## Architecture

### **Frontend (Streamlit)**

```
app/
├── src/
│   ├── Home.py              # Main entry point and role selection
│   ├── pages/               # Persona-specific pages
│   │   ├── doctor_home.py          # Doctor dashboard
│   │   ├── xx_Nurse_Dashboard.py   # Nurse dashboard
│   │   ├── proxy_home.py           # Proxy dashboard
│   │   ├── 50_Patient_Home.py      # Patient dashboard
│   │   ├── doctor_alerts.py        # Doctor alerts
│   │   ├── doctor_inbox.py         # Doctor messages
│   │   ├── doctor_patients.py      # Doctor patient management
│   │   ├── xx_Nurse_Alerts.py      # Nurse alerts
│   │   ├── xx_Nurse_Patients.py    # Nurse patient management
│   │   ├── xx_Nurse_Treatments.py  # Nurse treatment management
│   │   ├── proxy_billing.py        # Proxy billing
│   │   ├── proxy_messages.py       # Proxy messaging
│   │   ├── proxy_portal.py         # Proxy portal
│   │   ├── 51_Patient_Billing.py   # Patient billing
│   │   └── 52_Patient_Inbox.py     # Patient messaging
│   ├── modules/             # Navigation and utilities
│   │   ├── nav.py                  # Role-based navigation
│   │   └── styles.py               # Medical theme styling
│   └── assets/              # Images and static files
│       └── logo.png                # VitalFlow logo
```

### **Backend (Flask API)**

```
api/
├── backend/
│   ├── patient/             # Patient management endpoints
│   ├── doctor/              # Doctor-specific endpoints
│   ├── nurse/               # Nurse-specific endpoints
│   ├── proxy/               # Proxy management endpoints
│   ├── vital/               # Vital signs endpoints
│   ├── medication/          # Medication management
│   ├── insurance/           # Insurance and billing
│   ├── message/             # Communication system
│   ├── alert/               # Alert and notification system
│   ├── condition/           # Medical conditions
│   ├── discharge/           # Patient discharge
│   ├── visit/               # Patient visits
│   └── admin/               # Administrative functions
├── backend_app.py           # Main Flask application
└── requirements.txt         # Python dependencies
```

### **Database (MySQL)**

- **Patient Management** - Personal information, medical history
- **Healthcare Staff** - Doctors, nurses, and their specialties
- **Medical Records** - Vitals, conditions, medications, visits
- **Insurance & Billing** - Policies, deductibles, payment tracking
- **Communication** - Messages, alerts, and notifications

## Authentication & Roles

### **User Roles & Personas**

- **Doctor (Maya)** - Full patient access, medical records, prescribing, alerts, and patient management
- **Nurse (Nic)** - Patient care, vitals monitoring, care coordination, treatments, and alerts
- **Proxy (Nina Pesci)** - Dependent patient management, insurance, billing, and messaging
- **Patient (Joe)** - Personal health records, appointments, medications, and billing

### **Security Features**

- Role-based access control (RBAC)
- Secure API endpoints
- Session-based authentication

## 📱 User Interface

### **Design Principles**

- **Healthcare-First** - Designed specifically for medical workflows
- **Responsive** - Works on desktop, tablet, and mobile devices
- **Accessible** - Follows healthcare accessibility guidelines
- **Professional** - Clean, medical-grade interface with medical theme

### **Key Components**

- **Role Selection Homepage** - Easy persona switching for development/testing
- **Dashboard Overview** - Real-time metrics and insights
- **Patient Cards** - Quick access to patient information
- **Navigation Sidebar** - Role-specific menu options
- **Interactive Forms** - Easy data entry and management

## API Endpoints

### **Core Endpoints**

- `GET /patient/` - Retrieve patient list
- `GET /patient/<id>` - Get specific patient details
- `GET /patient/<id>/medications` - Get patient medications
- `GET /patient/<id>/vitals` - Get patient vital signs
- `GET /patient/<id>/condition` - Get patient conditions
- `GET /patient/<id>/discharge` - Get patient discharge info
- `GET /doctor/` - Get doctor information
- `GET /nurse/` - Get nurse information
- `GET /proxy/` - Get proxy information
- `GET /vital/` - Retrieve vital signs
- `GET /medication/` - Get medication data
- `GET /message/` - Get messages
- `POST /message/` - Send new messages
- `GET /alert/` - Retrieve alerts
- `GET /condition/` - Get medical conditions
- `GET /visit/` - Get patient visits
- `GET /discharge/` - Get discharge information
- `GET /insurance/` - Get insurance information

### **Authentication**

- All endpoints require proper authentication
- Role-based access control
- Secure token validation

## Database Schema

### **Key Tables**

- **Patients** - Personal and medical information
- **Doctors** - Healthcare provider details
- **Nurses** - Nursing staff information
- **Proxies** - Patient representatives
- **Visits** - Patient appointments and encounters
- **VitalChart** - Patient vital signs
- **Medications** - Prescription information
- **Insurance** - Policy and billing details
- **Conditions** - Medical conditions and diagnoses
- **Discharges** - Patient discharge information

## Deployment

### **Development/Testing**

```bash
# Start testing containers
docker-compose -f sandbox.yaml up -d

# Stop testing containers
docker-compose -f sandbox.yaml down
```

### **Production Deployment**

```bash
# Build and deploy
docker-compose up -d

# Scale services
docker-compose up -d --scale web=3
```

### **Environment Variables**

- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `DB_NAME` - Database name
- `SECRET_KEY` - Application secret key
- `API_BASE_URL` - Backend API URL

## Testing

### **API Testing**

```bash
# Test API endpoints
curl http://localhost:4000/patient

```

### **Frontend Testing**

- Navigate through different personas using the homepage role selection
- Test form submissions
- Verify data display
- Check responsive design
- Test role-based access control

## Monitoring & Logs

### **Application Logs**

- API request/response logging
- Streamlit application logging
- Database connection monitoring

## Contributing

### **Development Setup**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **Code Standards**

- Use meaningful commit messages
- Include proper documentation
- Test your changes thoroughly
- Follow the existing code structure

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

### **Documentation**

- [API Documentation](api/API_README.md)
- [Database Schema](database-files/)
- [User Guides](docs/)

---

## Getting Started Checklist

- [ ] Clone the repository
- [ ] Install Docker and Docker Compose
- [ ] Start the application with `docker-compose up -d`
- [ ] Access the frontend at http://localhost:8501
- [ ] Select your role from the homepage
- [ ] Explore the different portals and features

_VitalFlow - Streamlining healthcare, one patient at a time._
