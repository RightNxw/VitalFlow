## Patient Home Page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Patient Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

## Add logo and navigation
SideBarLinks()

## API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
def get_patient_info(patient_id):
    """Get patient information from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        st.error("Could not connect to patient API")
        return None

def get_patient_visit(patient_id):
    """Get patient's current visit from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/visit")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_patient_vitals(patient_id):
    """Get patient's current vitals from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/vitals")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_patient_medications(patient_id):
    """Get patient's medications from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/medications")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_new_visit(patient_id, admit_reason, appointment_date):
    """Create a new visit in the database"""
    try:
        visit_data = {
            "AdmitReason": admit_reason,
            "AppointmentDate": appointment_date.isoformat()
        }
        response = requests.post(f"{API_BASE_URL}/visits/visits", json=visit_data)
        if response.status_code == 201:
            visit_id = response.json().get("visit_id")
            if visit_id:
                # Link the visit to the patient
                update_data = {"VisitID": visit_id}
                update_response = requests.put(f"{API_BASE_URL}/patient/patients/{patient_id}", json=update_data)
                if update_response.status_code == 200:
                    return True
        return False
    except:
        return False

## Main page
st.markdown("# Patient Home Page!")

# Get current patient ID from session state (assuming patient is logged in)
patient_id = st.session_state.get('current_patient_id', 1)  # Default to patient ID 1 for demo

# Get patient data from database
patient_info = get_patient_info(patient_id)
if not patient_info:
    st.error("Could not load patient information")
    st.stop()

# Extract patient name from database
patient_name = f"{patient_info.get('FirstName', 'Unknown')} {patient_info.get('LastName', 'Unknown')}"
patient_dob = patient_info.get('DOB', 'Unknown')

# Create two columns: left sidebar and main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Welcome JOE,")
    
    # Navigation menu based on wireframe
    st.markdown("🏠 **Home**")
    st.markdown("❤️ **Portal**")
    st.markdown("💰 **Billing**")
    st.markdown("📬 **Inbox**")
    st.markdown("⚙️ **Settings**")

with col2:
    # Top section: Search and Hospital Info
    col2a, col2b = st.columns([3, 1])
    
    with col2a:
        st.markdown("**Search**")
        search_query = st.text_input("", placeholder="...", key="patient_search")
    
    with col2b:
        st.markdown("🔲 **HOSPITAL**")
    
    # Middle section: Patient Profile
    st.markdown("---")
    col2c, col2d = st.columns([1, 3])
    
    with col2c:
        st.markdown("👤")  # Generic user icon
    
    with col2d:
        st.markdown(f"**{patient_name}**")
        st.markdown(f"**Patient DOB:** {patient_dob}")
    
    # Bottom section: Visits
    st.markdown("---")
    st.markdown("### **VISITS**")
    
    # Get current visit from database
    current_visit = get_patient_visit(patient_id)
    
    if current_visit:
        # Display current visit info from database
        st.info("**Current Visit Information:**")
        st.markdown(f"**Patient Admit Date:** {current_visit.get('AppointmentDate', 'N/A')}")
        st.markdown(f"**Admit Reason:** {current_visit.get('AdmitReason', 'N/A')}")
        if current_visit.get('NextVisitDate'):
            st.markdown(f"**Next Visit:** {current_visit.get('NextVisitDate', 'N/A')}")
    else:
        st.info("No current visit found")
    
    # Form to create new visit
    st.markdown("**Schedule New Visit:**")
    with st.form("new_visit_form"):
        admit_reason = st.text_input("Admit Reason", placeholder="Enter reason for visit...")
        appointment_date = st.date_input("Appointment Date", value=datetime.now().date())
        
        if st.form_submit_button("Schedule Visit"):
            if admit_reason and appointment_date:
                if create_new_visit(patient_id, admit_reason, appointment_date):
                    st.success("Visit scheduled successfully!")
                    st.rerun()
                else:
                    st.error("Failed to schedule visit")
            else:
                st.error("Please fill in all fields")

# Display additional patient information from database
st.markdown("---")
st.markdown("### **Patient Information from Database**")

# Get vitals from database
vitals = get_patient_vitals(patient_id)
if vitals:
    st.markdown("**Current Vitals:**")
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    with col_v1:
        st.metric("Heart Rate", f"{vitals.get('HeartRate', 'N/A')} bpm")
    with col_v2:
        st.metric("Blood Pressure", vitals.get('BloodPressure', 'N/A'))
    with col_v3:
        st.metric("Temperature", f"{vitals.get('Temperature', 'N/A')}°F")
    with col_v4:
        st.metric("Respiratory Rate", f"{vitals.get('RespiratoryRate', 'N/A')} /min")
else:
    st.info("No vital signs recorded")

# Get medications from database
medications = get_patient_medications(patient_id)
if medications:
    st.markdown("**Current Medications:**")
    for med in medications:
        with st.expander(f"💊 {med.get('PrescriptionName', 'N/A')}"):
            st.markdown(f"**Dosage:** {med.get('DosageAmount', 'N/A')} {med.get('DosageUnit', '')}")
            st.markdown(f"**Frequency:** {med.get('FrequencyAmount', 'N/A')} {med.get('FrequencyPeriod', '')}")
            st.markdown(f"**Pickup Location:** {med.get('PickUpLocation', 'N/A')}")
else:
    st.info("No medications prescribed")
