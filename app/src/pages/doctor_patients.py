
## doctor patients page

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
    page_title="Doctor Portal - Patients",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

## App state for navigation
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None
if "current_view" not in st.session_state:
    st.session_state.current_view = "list"

## API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
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
        # Get patient basic info
        patient_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}")
        if patient_response.status_code != 200:
            return None
            
        patient = patient_response.json()
        
        # Get patient vitals
        vitals_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/vitals")
        vitals = vitals_response.json() if vitals_response.status_code == 200 else []
        
        # Get patient conditions
        conditions_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/condition")
        conditions = conditions_response.json() if conditions_response.status_code == 200 else []
        
        # Get patient medications
        meds_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/medications")
        medications = meds_response.json() if meds_response.status_code == 200 else []
        
        return {
            'patient': patient,
            'vitals': vitals,
            'conditions': conditions,
            'medications': medications
        }
    except:
        return None

def get_all_medications():
    """Get all available medications from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/medication/medications")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def update_patient_vitals(patient_id, vitals_data):
    """Update patient vitals"""
    try:
        response = requests.post(f"{API_BASE_URL}/vital/vitalcharts", json=vitals_data)
        return response.status_code == 201
    except:
        return False

def update_patient_medications(patient_id, medication_data):
    """Update patient medications"""
    try:
        response = requests.post(f"{API_BASE_URL}/medication/patient_medications", json=medication_data)
        return response.status_code == 201
    except:
        return False

## Main page logic
def main():
    if st.session_state.current_view == "list":
        show_patient_list()
    elif st.session_state.current_view == "details":
        show_patient_details()
    elif st.session_state.current_view == "chart":
        show_patient_chart()
    elif st.session_state.current_view == "medications":
        show_patient_medications()

def show_patient_list():
    """Show the main patient list with search and filtering"""
    st.write("# Patient Management")
    st.write("View and manage patient information.")
    
    # Get all patients
    patients = get_patients()
    
    if not patients:
        st.warning("No patients found.")
        st.stop()
    
    # Patient search and filtering
    col1, col2 = st.columns([3, 1])
    with col1:
        patient_filter = st.text_input("Filter patients", placeholder="Search by patient name...")
    with col2:
        sort_by = st.selectbox("Sort by", ["Name", "DOB", "Recent Visit"])
    
    # Filter patients by their names
    if patient_filter:
        filtered_patients = [
            p for p in patients 
            if patient_filter.lower() in f"{p.get('FirstName', '')} {p.get('LastName', '')}".lower()
        ]
    else:
        filtered_patients = patients
    
    # Display patient data
    if filtered_patients:
        st.markdown(f"### Showing {len(filtered_patients)} patients")
        
        # Create interactive patient cards instead of dataframe
        for patient in filtered_patients:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    **{patient.get('FirstName', 'N/A')} {patient.get('LastName', 'N/A')}**
                    - ID: {patient.get('PatientID', 'N/A')}
                    - DOB: {patient.get('DOB', 'N/A')}
                    - Blood Type: {patient.get('BloodType', 'N/A')}
                    - Weight: {patient.get('Weight', 'N/A')} lbs
                    """)
                
                with col2:
                    if st.button("📋 Details", key=f"details_{patient.get('PatientID')}", use_container_width=True):
                        st.session_state.selected_patient = patient.get('PatientID')
                        st.session_state.current_view = "details"
                        st.rerun()
                
                with col3:
                    if st.button("📊 Chart", key=f"chart_{patient.get('PatientID')}", use_container_width=True):
                        st.session_state.selected_patient = patient.get('PatientID')
                        st.session_state.current_view = "chart"
                        st.rerun()
                
                with col4:
                    if st.button("💊 Meds", key=f"meds_{patient.get('PatientID')}", use_container_width=True):
                        st.session_state.selected_patient = patient.get('PatientID')
                        st.session_state.current_view = "medications"
                        st.rerun()
                
                st.divider()
    else:
        st.info("No patients match your search criteria.")

def show_patient_details():
    """Show detailed patient information"""
    if not st.session_state.selected_patient:
        st.error("No patient selected")
        return
    
    patient_id = st.session_state.selected_patient
    patient_data = get_patient_details(patient_id)
    
    if not patient_data:
        st.error("Could not load patient data")
        return
    
    patient = patient_data['patient']
    vitals = patient_data['vitals']
    conditions = patient_data['conditions']
    medications = patient_data['medications']
    
    # Header with back button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 📋 Patient Details: {patient.get('FirstName', '')} {patient.get('LastName', '')}")
    with col2:
        if st.button("← Back to List"):
            st.session_state.current_view = "list"
            st.rerun()
    
    # Patient information tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Basic Info", "❤️ Vitals", "🏥 Conditions", "💊 Medications"])
    
    with tab1:
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            - **Patient ID:** {patient.get('PatientID', 'N/A')}
            - **First Name:** {patient.get('FirstName', 'N/A')}
            - **Last Name:** {patient.get('LastName', 'N/A')}
            - **Date of Birth:** {patient.get('DOB', 'N/A')}
            """)
        
        with col2:
            st.markdown(f"""
            - **Blood Type:** {patient.get('BloodType', 'N/A')}
            - **Weight:** {patient.get('Weight', 'N/A')} lbs
            - **Pre-existing Conditions:** {patient.get('PreExisting', 'N/A')}
            """)
    
    with tab2:
        st.markdown("### Vital Signs")
        if vitals:
            for vital in vitals:
                # Safe timestamp handling
                timestamp = vital.get('Timestamp', 'N/A')
                if timestamp and timestamp != 'N/A':
                    try:
                        # Try to format the timestamp if it's valid
                        if isinstance(timestamp, str):
                            timestamp_str = timestamp
                        else:
                            timestamp_str = str(timestamp)
                    except:
                        timestamp_str = 'Unknown Time'
                else:
                    timestamp_str = 'No Timestamp'
                
                with st.expander(f"Vital Record - {timestamp_str}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Heart Rate", f"{vital.get('HeartRate', 'N/A')} bpm")
                        st.metric("Blood Pressure", vital.get('BloodPressure', 'N/A'))
                    with col2:
                        st.metric("Temperature", f"{vital.get('Temperature', 'N/A')}°F")
                        st.metric("Respiratory Rate", f"{vital.get('RespiratoryRate', 'N/A')} /min")
        else:
            st.info("No vital records found")
    
    with tab3:
        st.markdown("### Medical Conditions")
        if conditions:
            for condition in conditions:
                with st.expander(f"Condition: {condition.get('Description', 'N/A')}"):
                    st.markdown(f"**Treatment:** {condition.get('Treatment', 'N/A')}")
        else:
            st.info("No conditions found")
    
    with tab4:
        st.markdown("### Current Medications")
        if medications:
            # Create DataFrame for better display
            df_m = pd.DataFrame(medications)
            if not df_m.empty:
                # Friendly column order if present
                order = [
                    "PrescriptionName", "DosageAmount", "DosageUnit", "FrequencyAmount", "FrequencyPeriod",
                    "PickUpLocation", "RefillsLeft", "PrescribedDate", "EndDate", "MedicationID"
                ]
                cols = [c for c in order if c in df_m.columns]
                # Ensure date-like columns render nicely
                for c in ["PrescribedDate", "EndDate"]:
                    if c in df_m.columns:
                        df_m[c] = pd.to_datetime(df_m[c], errors="coerce").dt.date
                
                st.dataframe(df_m[cols] if cols else df_m, use_container_width=True, hide_index=True)
            else:
                st.info("No medications found")
        else:
            st.info("No medications found")

def show_patient_chart():
    """Show and edit patient chart/vitals"""
    if not st.session_state.selected_patient:
        st.error("No patient selected")
        return
    
    patient_id = st.session_state.selected_patient
    patient_data = get_patient_details(patient_id)
    
    if not patient_data:
        st.error("Could not load patient data")
        return
    
    patient = patient_data['patient']
    vitals = patient_data['vitals']
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 📊 Patient Chart: {patient.get('FirstName', '')} {patient.get('LastName', '')}")
    with col2:
        if st.button("← Back to List"):
            st.session_state.current_view = "list"
            st.rerun()
    
    # Current vitals display
    st.markdown("### Current Vital Signs")
    if vitals and len(vitals) > 0:
        latest_vital = vitals[-1]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Heart Rate", f"{latest_vital.get('HeartRate', 'N/A')} bpm")
        with col2:
            st.metric("Blood Pressure", latest_vital.get('BloodPressure', 'N/A'))
        with col3:
            st.metric("Temperature", f"{latest_vital.get('Temperature', 'N/A')}°F")
        with col4:
            st.metric("Respiratory Rate", f"{latest_vital.get('RespiratoryRate', 'N/A')} /min")
    else:
        st.info("No vital records found")
    
    # Add new vitals
    st.markdown("### Add New Vital Signs")
    with st.form("new_vitals"):
        col1, col2 = st.columns(2)
        with col1:
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=300, value=72)
            blood_pressure = st.text_input("Blood Pressure", placeholder="120/80")
            temperature = st.number_input("Temperature (°F)", min_value=90.0, max_value=110.0, value=98.6, step=0.1)
        with col2:
            respiratory_rate = st.number_input("Respiratory Rate (/min)", min_value=0, max_value=60, value=16)
            oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=70, max_value=100, value=98)
            timestamp = st.datetime_input("Timestamp", value=datetime.now())
        
        if st.form_submit_button("💾 Save Vitals"):
            new_vitals = {
                "PatientID": patient_id,
                "HeartRate": heart_rate,
                "BloodPressure": blood_pressure,
                "Temperature": temperature,
                "RespiratoryRate": respiratory_rate,
                "Timestamp": timestamp.isoformat()
            }
            
            if update_patient_vitals(patient_id, new_vitals):
                st.success("Vitals saved successfully!")
                st.rerun()
            else:
                st.error("Failed to save vitals")

def show_patient_medications():
    """Show and manage patient medications"""
    if not st.session_state.selected_patient:
        st.error("No patient selected")
        return
    
    patient_id = st.session_state.selected_patient
    patient_data = get_patient_details(patient_id)
    
    if not patient_data:
        st.error("Could not load patient data")
        return
    
    patient = patient_data['patient']
    medications = patient_data['medications']
    all_meds = get_all_medications()
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 💊 Medications: {patient.get('FirstName', '')} {patient.get('LastName', '')}")
    with col2:
        if st.button("← Back to List"):
            st.session_state.current_view = "list"
            st.rerun()
    
    # Current medications
    st.markdown("### Current Medications")
    if medications:
        for med in medications:
            with st.expander(f"💊 {med.get('MedicationName', 'N/A')}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    **Dosage:** {med.get('Dosage', 'N/A')}  
                    **Frequency:** {med.get('Frequency', 'N/A')}  
                    **Start Date:** {med.get('StartDate', 'N/A')}  
                    **End Date:** {med.get('EndDate', 'N/A')}  
                    **Instructions:** {med.get('Instructions', 'N/A')}
                    """)
                with col2:
                    if st.button("❌ Remove", key=f"remove_{med.get('PatientMedicationID')}"):
                        st.info("Remove functionality would be implemented here")
    else:
        st.info("No current medications")
    
    # Add new medication
    st.markdown("### Prescribe New Medication")
    with st.form("new_medication"):
        col1, col2 = st.columns(2)
        with col1:
            if all_meds:
                medication_options = [f"{m.get('MedicationName', 'N/A')} - {m.get('Strength', 'N/A')}" for m in all_meds]
                selected_med = st.selectbox("Select Medication", medication_options)
            else:
                selected_med = st.text_input("Medication Name", placeholder="e.g., Lisinopril")
            
            dosage = st.text_input("Dosage", placeholder="e.g., 10mg")
            frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
        
        with col2:
            start_date = st.date_input("Start Date", value=datetime.now().date())
            end_date = st.date_input("End Date", value=datetime.now().date())
            instructions = st.text_area("Instructions", placeholder="Take with food, avoid alcohol...")
        
        if st.form_submit_button("💾 Prescribe Medication"):
            st.success("Medication prescribed successfully!")
            st.info("Note: This would save to the API in a real implementation")

## Run the main app
if __name__ == "__main__":
    main()