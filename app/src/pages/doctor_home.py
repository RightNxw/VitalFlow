

## doctor Home Page
 
import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.styles import apply_page_styling, create_metric_card, create_patient_card, create_medical_divider
 
## Apply medical theme and styling
apply_page_styling()
 
## Add logo and navigation
SideBarLinks()
 
# Medical-themed header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">👨‍⚕️ Doctor Portal</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        Manage patients, view alerts, and access medical records
    </p>
</div>
""", unsafe_allow_html=True)
 
# API configuration
API_BASE_URL = "http://web-api:4000"

## Patient card renderer with clickable functionality
def render_patient_card(patient_data):
    """Render a clickable patient card with detailed information"""
    if not patient_data:
        return

    patient = patient_data.get('patient', {})
    visits = patient_data.get('visits', [])
    vitals = patient_data.get('vitals', [])
    conditions = patient_data.get('conditions', [])
    medications = patient_data.get('medications', [])

    ## Get admit date - check multiple sources
    admit_date = 'N/A'
    
    # First check if patient has a direct VisitID
    if patient.get('VisitID'):
        try:
            visit_response = requests.get(f"{API_BASE_URL}/visit/{patient.get('VisitID')}")
            if visit_response.status_code == 200:
                visit_data = visit_response.json()
                admit_date = visit_data.get('AppointmentDate', 'N/A')
        except:
            pass
    
    # If no direct visit, check the visits list
    if admit_date == 'N/A' and visits:
        latest_visit = visits[-1] if len(visits) > 0 else {}
        admit_date = latest_visit.get('AppointmentDate', 'N/A')
    
    # Format the admit date if we have one
    if admit_date and admit_date != 'N/A':
        try:
            # Handle different date formats
            if isinstance(admit_date, str):
                if 'T' in admit_date:  # ISO format
                    admit_date = datetime.fromisoformat(admit_date.replace('Z', '+00:00')).strftime('%m/%d/%Y')
                else:  # Date only format
                    admit_date = datetime.strptime(admit_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        except:
            admit_date = str(admit_date)

    ## Get patient initials for avatar
    first_name = patient.get('FirstName', '')
    last_name = patient.get('LastName', '')
    initials = f"{first_name[0] if first_name else 'P'}{last_name[0] if last_name else 'T'}"

    ## Create expandable patient card
    with st.expander(f"👤 {patient.get('FirstName', 'N/A')} {patient.get('LastName', 'N/A')} - Admitted: {admit_date}", expanded=False):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #333; 
                     display: flex; align-items: center; justify-content: center; 
                     font-size: 32px; background: #f8f9fa; margin: 0 auto;">
                    {initials}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            ## Basic patient information
            st.markdown("#### Patient Information")
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write(f"**Patient ID:** {patient.get('PatientID', 'N/A')}")
                st.write(f"**Date of Birth:** {patient.get('DOB', 'N/A')}")
                st.write(f"**Blood Type:** {patient.get('BloodType', 'N/A')}")
            
            with col_info2:
                st.write(f"**Weight:** {patient.get('Weight', 'N/A')} lbs")
                st.write(f"**Visit Status:** {visits[-1].get('Status', 'N/A') if visits else 'N/A'}")
                st.write(f"**Next Visit:** {visits[-1].get('NextVisitDate', 'N/A') if visits else 'N/A'}")
            
            ## Patient medications
            if medications and len(medications) > 0:
                st.markdown("#### Current Medications")
                try:
                    # Ensure medications is a list of dictionaries
                    if isinstance(medications, list) and all(isinstance(m, dict) for m in medications):
                        meds_df = pd.DataFrame(medications)
                        st.dataframe(meds_df, use_container_width=True)
                    else:
                        st.info("Medications data format not supported")
                except Exception as e:
                    st.error(f"Error displaying medications: {str(e)}")
 
## API functions with proper error handling
def get_doctors():
    """Get all doctors from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/doctor/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to doctors API, using dummy data.")
        return [{"DoctorID": 1, "FirstName": "Maya", "LastName": "Ellison"}]
 
def get_patients():
    """Get all patients from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/")
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
        patient_response = requests.get(f"{API_BASE_URL}/patient/{patient_id}")
        if patient_response.status_code != 200:
            return None
 
        patient = patient_response.json()
 
        ## Get patient vitals
        try:
            vitals_response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/vitals")
            vitals = vitals_response.json() if vitals_response.status_code == 200 else []
        except:
            vitals = []
 
        ## Get patient conditions
        try:
            conditions_response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/condition")
            conditions = conditions_response.json() if conditions_response.status_code == 200 else []
        except:
            conditions = []
 
        ## Get patient medications
        try:
            meds_response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/medications")
            medications = meds_response.json() if meds_response.status_code == 200 else []
        except:
            medications = []
 
        ## Get patient visits - try multiple approaches
        patient_visits = []
        
        # Method 1: Get all visits and filter by patient ID
        try:
            visits_response = requests.get(f"{API_BASE_URL}/visit/")
            if visits_response.status_code == 200:
                all_visits = visits_response.json()
                patient_visits = [v for v in all_visits if v.get('PatientID') == patient_id]
        except:
            pass
        
        # Method 2: If patient has VisitID, get that specific visit
        if not patient_visits and patient.get('VisitID'):
            try:
                specific_visit_response = requests.get(f"{API_BASE_URL}/visit/{patient.get('VisitID')}")
                if specific_visit_response.status_code == 200:
                    specific_visit = specific_visit_response.json()
                    patient_visits = [specific_visit]
            except:
                pass
 
        return {
            'patient': patient,
            'vitals': vitals,
            'conditions': conditions,
            'medications': medications,
            'visits': patient_visits
        }
    except Exception as e:
        return None
 
def get_visits():
    """Get all visits from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/visit/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to visits API, using dummy data.")
        return [
            {"VisitID": 1, "PatientID": 1, "Status": "Active", "AppointmentDate": "2024-01-15"},
            {"VisitID": 2, "PatientID": 2, "Status": "Active", "AppointmentDate": "2024-01-20"},
            {"VisitID": 3, "PatientID": 1, "Status": "Scheduled", "AppointmentDate": "2024-02-01", "NextVisitDate": "2024-02-01"}
        ]
 
def get_vitals():
    """Get all vital charts from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/vital/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to vitals API, using dummy data.")
        return [{"VitalID": 1, "PatientID": 1, "HeartRate": 75, "BloodPressure": "120/80"}]
 
def get_conditions():
    """Get all conditions from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/condition/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to conditions API, using dummy data.")
        return [{"ConditionID": 1, "PatientID": 1, "Condition": "Hypertension", "Severity": "Mild"}]
 
def get_alerts():
    """Get all alerts - doctors and nurses see the same alerts"""
    try:
        response = requests.get(f"{API_BASE_URL}/alert/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [{"AlertID": 1, "Title": "High Blood Pressure", "Description": "Patient BP elevated", "Severity": "High"}]
 
def get_messages(doctor_id):
    """Get messages for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/message/?user_type=doctor&user_id={doctor_id}")
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
 
## Consolidated search functionality
st.markdown("### Patient Search & Management")
patient_search = st.text_input("Search Patients", placeholder="Search patients by name...", label_visibility="visible")
 
## Get all patients and filter based on search
all_patients = get_patients()
if patient_search:
    # Search patients by their names
    filtered_patients = []
    if all_patients:
        for patient in all_patients:
            full_name = f"{patient.get('FirstName', '')} {patient.get('LastName', '')}".lower()
            if patient_search.lower() in full_name:
                filtered_patients.append(patient)
 
    if filtered_patients:
        st.info(f"Found {len(filtered_patients)} patients matching '{patient_search}'")
    else:
        st.warning(f"No patients found matching '{patient_search}'")
        filtered_patients = []
else:
    filtered_patients = all_patients if all_patients else []
 
## Display patient cards
if filtered_patients:
    for patient in filtered_patients:
        patient_details = get_patient_details(patient.get('PatientID'))
        if patient_details:
            render_patient_card(patient_details)
else:
    st.info("No patient data available.")
 