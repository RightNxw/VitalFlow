## Proxy Portal - Patient Care Plans for given proxy's patients

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
    page_title="Proxy Portal - Patient Care",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("# 👥 Patient Care Plan Portal")
st.write("View and manage care plans for your dependent patients.")

# API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
def get_proxies():
    """Get all proxies from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxies")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to proxies API, using dummy data.")
        return [{"ProxyID": 1, "FirstName": "Nina", "LastName": "Pesci", "Relationship": "Child"}]

def get_proxy_patients(proxy_id):
    """Get patients for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxies/{proxy_id}/patients")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to proxy patients API, using dummy data.")
        return [
            {"PatientID": 1, "FirstName": "Joe", "LastName": "Pesci", "DOB": "1970-05-15", "BloodType": "O-"},
            {"PatientID": 2, "FirstName": "Maria", "LastName": "Pesci", "DOB": "1975-08-22", "BloodType": "A+"}
        ]

def get_patient_details(patient_id):
    """Get detailed patient information"""
    try:
        patient_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}")
        if patient_response.status_code != 200:
            return None

        patient = patient_response.json()

        # Get patient vitals
        try:
            vitals_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/vitals")
            vitals = vitals_response.json() if vitals_response.status_code == 200 else []
        except:
            vitals = []

        # Get patient conditions
        try:
            conditions_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/condition")
            conditions = conditions_response.json() if conditions_response.status_code == 200 else []
        except:
            conditions = []

        # Get patient medications
        try:
            meds_response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/medications")
            medications = meds_response.json() if meds_response.status_code == 200 else []
        except:
            medications = []

        return {
            'patient': patient,
            'vitals': vitals,
            'conditions': conditions,
            'medications': medications
        }
    except:
        return None

## Get proxy information
proxies = get_proxies()
if proxies:
    current_proxy = proxies[0]
    proxy_id = current_proxy.get('ProxyID', 1)
else:
    proxy_id = 1

## Welcome message
if proxies:
    proxy_name = f"{proxies[0].get('FirstName', 'Nina')} {proxies[0].get('LastName', 'Pesci')}"
    st.markdown(f"### Welcome, {proxy_name}")
else:
    st.markdown("### Welcome, Nina Pesci")

st.markdown("---")

## Patient Care Plans
st.markdown("## 🏥 Patient Care Plans")

dependent_patients = get_proxy_patients(proxy_id)

if dependent_patients:
    for patient in dependent_patients:
        with st.expander(f"{patient.get('FirstName', '')} {patient.get('LastName', '')} - Care Plan", expanded=True):
            patient_details = get_patient_details(patient.get('PatientID'))
            
            if patient_details:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📋 Patient Information")
                    patient_info = patient_details.get('patient', {})
                    st.markdown(f"""
                    **Name:** {patient_info.get('FirstName', '')} {patient_info.get('LastName', '')}
                    **Date of Birth:** {patient_info.get('DOB', 'N/A')}
                    **Blood Type:** {patient_info.get('BloodType', 'N/A')}
                    **Emergency Contact:** {patient_info.get('EmergencyContact', 'N/A')}
                    """)
                    
                with col2:
                    st.markdown("### 💊 Current Medications")
                    medications = patient_details.get('medications', [])
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
                        st.info("No current medications")
                    
            
            st.divider()
else:
    st.info("No dependent patients found for care plan information.")
