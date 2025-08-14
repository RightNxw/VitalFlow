# VitalFlow - Healthcare Portal

A comprehensive healthcare management system built with Streamlit frontend and Flask API backend, designed to streamline patient care, billing, and communication between healthcare providers and patients.

## Features

### **Multi-Persona Access**
- ** Doctor Portal** - Patient management, medical charts, alerts, and communications
- ** Nurse Portal** - Patient care, vitals monitoring, and care coordination
- ** Proxy Portal** - Manage dependent patients, insurance, and billing
- ** Patient Portal** - Personal health records, medications, and appointments

### **Core Functionality**
- **Patient Management** - Comprehensive patient records and medical history
- **Insurance & Billing** - Policy management and deductible tracking
- **Communication System** - Secure messaging between healthcare teams
- **Medical Records** - Vitals, conditions, medications, and visit tracking
- **Alert System** - Medical alerts and notifications
- **Dashboard Analytics** - Real-time metrics and insights

##  Quick Start

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

3. **Start the application**
   ```bash
   # Start all services
   docker-compose up -d
   
   # Or use sandbox configuration for testing
   docker-compose -f sandbox.yaml up -d
   ```

4. **Access the application**
   - **Frontend**: http://localhost:8501
   - **API**: http://localhost:4000
   - **Database**: localhost:3306

## Architecture

### **Frontend (Streamlit)**
```
app/
├── src/
│   ├── pages/           # Persona-specific pages
│   │   ├── doctor_home.py      # Doctor dashboard
│   │   ├── nurse_home.py       # Nurse dashboard
│   │   ├── proxy_home.py       # Proxy dashboard
│   │   ├── patient_home.py     # Patient dashboard
│   │   └── admin_home.py       # Admin dashboard
│   ├── modules/         # Navigation and utilities
│   │   └── nav.py              # Role-based navigation
│   └── assets/          # Images and static files
│       └── logo.png            # VitalFlow logo
```

### **Backend (Flask API)**
```
api/
├── backend/
│   ├── patient/         # Patient management endpoints
│   ├── doctor/          # Doctor-specific endpoints
│   ├── nurse/           # Nurse-specific endpoints
│   ├── proxy/           # Proxy management endpoints
│   ├── vital/           # Vital signs endpoints
│   ├── medication/      # Medication management
│   ├── insurance/       # Insurance and billing
│   ├── message/         # Communication system
│   └── alert/           # Alert and notification system
├── backend_app.py       # Main Flask application
└── requirements.txt     # Python dependencies
```

## ** Key Changes Made:**

1. **Updated title** from "CS 3200 Project Template" to "VitalFlow - Healthcare Portal"
2. **Added healthcare-specific features** and functionality
3. **Updated architecture** to reflect your actual project structure
4. **Added proper persona descriptions** (Doctor, Nurse, Proxy, Patient)
5. **Updated API endpoints** to match your actual backend
6. **Added healthcare-specific sections** like medical records, insurance, etc.
7. **Updated deployment instructions** to include your sandbox.yaml
8. **Added proper project branding** and description

### **Database (MySQL)**
- **Patient Management** - Personal information, medical history
- **Healthcare Staff** - Doctors, nurses, and their specialties
- **Medical Records** - Vitals, conditions, medications, visits
- **Insurance & Billing** - Policies, deductibles, payment tracking
- **Communication** - Messages, alerts, and notifications

## Authentication & Roles

### **User Roles**
- **Doctor** - Full patient access, medical records, prescribing
- **Nurse** - Patient care, vitals monitoring, care coordination
- **Proxy** - Dependent patient management, insurance, billing
- **Patient** - Personal health records, appointments, medications

### **Security Features**
- Role-based access control (RBAC)
- Secure API endpoints


## 📱 User Interface

### **Design Principles**
- **Healthcare-First** - Designed specifically for medical workflows
- **Responsive** - Works on desktop, tablet, and mobile devices
- **Accessible** - Follows healthcare accessibility guidelines
- **Professional** - Clean, medical-grade interface

### **Key Components**
- **Dashboard Overview** - Real-time metrics and insights
- **Patient Cards** - Quick access to patient information
- **Navigation Sidebar** - Role-specific menu options
- **Interactive Forms** - Easy data entry and management

## API Endpoints

### **Core Endpoints**
- `GET /patient/patients` - Retrieve patient list
- `GET /doctor/` - Get doctor information
- `GET /nurse/` - Get nurse information
- `GET /proxy/` - Get proxy information
- `GET /vital/vitalcharts` - Retrieve vital signs
- `GET /medication/medications` - Get medication data
- `POST /message/` - Send new messages
- `GET /alert/alerts` - Retrieve alerts

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
curl http://localhost:4000/patient/patients

# Test with authentication
curl -H "Authorization: Bearer <token>" http://localhost:4000/doctor/
```

### **Frontend Testing**
- Navigate through different personas
- Test form submissions
- Verify data display
- Check responsive design

## Monitoring & Logs

### **Application Logs**
- API request/response logging



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

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

### **Documentation**
- [API Documentation](api/API_README.md)
- [Database Schema](database-files/)
- [User Guides](docs/)



### **Contact**
- **Project Maintainer**: [Sophia Ray]
- **Email**: [ray.soph@northeastern.edy]
- **GitHub**: [sophiaray21]





---

## Getting Started Checklist




*VitalFlow - Streamlining healthcare, one patient at a time.*