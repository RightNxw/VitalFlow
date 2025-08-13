

## doctor Home Page
 
import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
 
## Add logo and navigation
SideBarLinks()
 
## Page config
st.set_page_config(
    page_title="Doctor Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
st.write("# Doctor Portal")
st.write("Manage patients, view alerts, and access medical records.")
 
# API configuration
API_BASE_URL = "http://web-api:4000"
 
# Custom CSS
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      [data-testid="stSidebar"] {width: 260px;}
      [data-baseweb="radio"] > div {row-gap: .35rem;}
 
      .patient-card {
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        background: white;
      }
 
      .patient-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 2px solid #333;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20px;
        font-size: 24px;
        background: #f8f9fa;
      }
 
      .patient-info {
        flex-grow: 1;
        line-height: 1.6;
      }
 
      .patient-field {
        margin: 4px 0;
        font-weight: 500;
      }
 
      .metric-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
      }
 
      .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0068c9;
      }
 
      .metric-label {
        color: #666;
        margin-top: 8px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)
 
 
 
## API functions with proper error handling
def get_doctors():
    """Get all doctors from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/doctors")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to doctors API, using dummy data.")
        return [{"DoctorID": 1, "FirstName": "Maya", "LastName": "Ellison"}]
 
def get_patients():
    """Get all patients from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to patients API, using dummy data.")
        return [
            {"PatientID": 1, "FirstName": "Jane", "LastName": "Doe", "DOB": "1990-01-01", "BloodType": "O+", "Weight": 150},
            {"PatientID": 2, "FirstName": "John", "LastName": "Smith", "DOB": "1985-05-15", "BloodType": "A-", "Weight": 180}
        ]
 
def get_patient_details(patient_id):
    """Get detailed patient information"""
    try:
        ## Get patient basic info
        patient_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}")
        if patient_response.status_code != 200:
            return None
 
        patient = patient_response.json()
 
        ## Get patient vitals
        try:
            vitals_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/vitals")
            vitals = vitals_response.json() if vitals_response.status_code == 200 else []
        except:
            vitals = []
 
        ## Get patient conditions
        try:
            conditions_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/condition")
            conditions = conditions_response.json() if conditions_response.status_code == 200 else []
        except:
            conditions = []
 
        ## Get patient medications
        try:
            meds_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/medications")
            medications = meds_response.json() if meds_response.status_code == 200 else []
        except:
            medications = []
 
        ## Get patient visits
        try:
            visits_response = requests.get(f"{API_BASE_URL}/visit/visits")
            visits = visits_response.json() if visits_response.status_code == 200 else []
            patient_visits = [v for v in visits if v.get('PatientID') == patient_id]
        except:
            patient_visits = []
 
        return {
            'patient': patient,
            'vitals': vitals,
            'conditions': conditions,
            'medications': medications,
            'visits': patient_visits
        }
    except:
        return None
 
def get_visits():
    """Get all visits from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/visit/visits")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to visits API, using dummy data.")
        return [{"VisitID": 1, "PatientID": 1, "Status": "Active", "AppointmentDate": "2024-01-15"}]
 
def get_vitals():
    """Get all vital charts from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/vital/vitalcharts")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to vitals API, using dummy data.")
        return [{"VitalID": 1, "PatientID": 1, "HeartRate": 75, "BloodPressure": "120/80"}]
 
def get_conditions():
    """Get all conditions from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/condition/conditions")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to conditions API, using dummy data.")
        return [{"ConditionID": 1, "PatientID": 1, "Condition": "Hypertension", "Severity": "Mild"}]
 
def get_alerts(doctor_id):
    """Get alerts for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/alerts?user_type=doctor&user_id={doctor_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [{"AlertID": 1, "Title": "High Blood Pressure", "Description": "Patient BP elevated", "Severity": "High"}]
 
def get_messages(doctor_id):
    """Get messages for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/messages?user_type=doctor&user_id={doctor_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [{"MessageID": 1, "Subject": "Patient Update", "Content": "Patient condition improved", "Priority": "Normal"}]
 
## Get doctor information for the current session
doctors = get_doctors()
if doctors:
    current_doctor = doctors[0]
    st.session_state.current_doctor_id = current_doctor.get('DoctorID', 1)
else:
    st.session_state.current_doctor_id = 1
 
## Welcome message
if doctors:
    doctor_name = f"Dr. {doctors[0].get('LastName', 'Ellison')}"
    st.markdown(f"### Welcome, {doctor_name}")
else:
    st.markdown("### Welcome, Dr. Ellison")
 
 
 
##  search bar
top_left, top_spacer, top_right = st.columns([6, 1, 1])
with top_left:
    global_search = st.text_input("Search", placeholder="Search patients, conditions, medications...", label_visibility="visible")
 
## Patient card renderer
def render_patient_card(patient_data):
    """Render a patient card with simplified information"""
    if not patient_data:
        return

    patient = patient_data.get('patient', {})
    visits = patient_data.get('visits', [])

    ## Get latest visit for admit date
    latest_visit = visits[-1] if len(visits) > 0 else {}

    ## Format admit date
    admit_date = latest_visit.get('AppointmentDate', 'N/A')
    if admit_date and admit_date != 'N/A':
        try:
            admit_date = datetime.strptime(admit_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        except:
            pass

    ## Get patient initials for avatar
    first_name = patient.get('FirstName', '')
    last_name = patient.get('LastName', '')
    initials = f"{first_name[0] if first_name else 'P'}{last_name[0] if last_name else 'T'}"

    card_html = f"""
    <div class="patient-card">
        <div class="patient-avatar">{initials}</div>
        <div class="patient-info">
            <div class="patient-field">Patient Name: <strong>{patient.get('FirstName', 'N/A')} {patient.get('LastName', 'N/A')}</strong></div>
            <div class="patient-field">Admit Date: <strong>{admit_date}</strong></div>
        </div>
    </div>
    """

    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.markdown(card_html, unsafe_allow_html=True)
    with col2:
        if st.button("📊 Chart", key=f"chart_{patient.get('PatientID')}", use_container_width=True):
            st.session_state.selected_patient = patient.get('PatientID')
            st.session_state.page = "👥 Patients"
            st.rerun()
    with col3:
        if st.button("💊 Meds", key=f"meds_{patient.get('PatientID')}", use_container_width=True):
            st.info(f"Medications for {patient.get('FirstName', 'Patient')}")
 
## Dashboard Overview
st.markdown("### Dashboard Overview")
 
## Dashboard metrics
col1, col2, col3, col4 = st.columns(4)
 
with col1:
    patients = get_patients()
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(patients) if patients else 0}</div>
            <div class="metric-label">Total Patients</div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
with col2:
    visits = get_visits()
    active_visits = len([v for v in visits if v.get('Status') == 'Active']) if visits else 0
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{active_visits}</div>
            <div class="metric-label">Active Visits</div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
with col3:
    vitals = get_vitals()
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(vitals) if vitals else 0}</div>
            <div class="metric-label">Vital Records</div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
with col4:
    conditions = get_conditions()
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(conditions) if conditions else 0}</div>
            <div class="metric-label">Conditions</div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
st.markdown("---")
 
# Patient search and list
patient_search = st.text_input("Patient Search", placeholder="Search patients by name...", label_visibility="visible")
 
st.markdown("### Recent Patients")
 
if patient_search:
    # Search patients by their names
    filtered_patients = []
    if patients:
        for patient in patients:
            full_name = f"{patient.get('FirstName', '')} {patient.get('LastName', '')}".lower()
            if patient_search.lower() in full_name:
                filtered_patients.append(patient)
 
    if filtered_patients:
        st.info(f"Found {len(filtered_patients)} patients matching '{patient_search}'")
    else:
        st.warning(f"No patients found matching '{patient_search}'")
        filtered_patients = patients[:4]  # Show default list
else:
    filtered_patients = patients[:4] if patients else []
 
# Get patient details and render patient cards
if filtered_patients:
    for patient in filtered_patients:
        patient_details = get_patient_details(patient.get('PatientID'))
        render_patient_card(patient_details)
else:
    st.info("No patient data available.")
 