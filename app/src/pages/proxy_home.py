## Proxy Home Page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Page config - MUST be first Streamlit command
from modules.styles import apply_page_styling, create_metric_card, create_patient_card, create_medical_divider

apply_page_styling()

## Add logo and navigation
SideBarLinks()

# Medical-themed header with icon
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">🏥 Proxy Home</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        Manage patient information and billing for your dependents
    </p>
</div>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://web-api:4000"

## API functions with proper error handling
def get_proxies():
    """Get all proxies from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxy/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to proxies API, using dummy data.")
        return [{"ProxyID": 1, "FirstName": "Nina", "LastName": "Pesci", "Relationship": "Child"}]

def get_proxy_patients(proxy_id):
    """Get patients for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxy/{proxy_id}/patients")
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

        ## Get patient visits
        try:
            visits_response = requests.get(f"{API_BASE_URL}/visit/")
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

def get_insurance_info(patient_id):
    """Get insurance information for patient"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/insurance")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to insurance API, using dummy data.")
        return [{"InsuranceProvider": "Blue Cross", "PolicyNumber": "BC123456", "Deductible": 1000.00}]



def get_messages(proxy_id):
    """Get messages for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/message/?user_type=proxy&user_id={proxy_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [{"MessageID": 1, "Subject": "Appointment Reminder", "Content": "Patient has appointment tomorrow", "Priority": "Normal"}]

## Get proxy information for the current session
proxies = get_proxies()
if proxies:
    current_proxy = proxies[0]
    st.session_state.current_proxy_id = current_proxy.get('ProxyID', 1)
else:
    st.session_state.current_proxy_id = 1

## Welcome message
if proxies:
    proxy_name = f"{proxies[0].get('FirstName', 'Nina')} {proxies[0].get('LastName', 'Pesci')}"
    # Get patient count for display
    proxy_id = st.session_state.get('current_proxy_id', 1)
    dependent_patients = get_proxy_patients(proxy_id)
    patient_count = len(dependent_patients) if dependent_patients else 0
    
    st.markdown(f"""
    <div class="medical-card" style="text-align: center; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);">
        <h2 style="margin: 0 0 1rem 0; color: var(--primary-blue);">👋 Welcome, {proxy_name}</h2>
        <p style="margin: 0; color: var(--gray-600); font-size: 1.1rem;">
            You're managing <strong>{patient_count}</strong> dependent patients
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="medical-card" style="text-align: center; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);">
        <h2 style="margin: 0 0 1rem 0; color: var(--primary-blue);">👋 Welcome, Nina Pesci</h2>
        <p style="margin: 0; color: var(--gray-600); font-size: 1.1rem;">
            You're managing dependent patients
        </p>
    </div>
    """, unsafe_allow_html=True)

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

    # Get additional patient info for enhanced display
    dob = patient.get('DOB', 'N/A')
    blood_type = patient.get('BloodType', 'N/A')
    
    # Format DOB if available
    if dob and dob != 'N/A':
        try:
            dob_formatted = datetime.strptime(dob, '%Y-%m-%d').strftime('%m/%d/%Y')
        except:
            dob_formatted = dob
    else:
        dob_formatted = 'N/A'

    card_html = f"""
    <div class="patient-card">
        <div class="patient-avatar">{initials}</div>
        <div class="patient-info">
            <div class="patient-field">
                <strong style="font-size: 1.1rem; color: var(--primary-blue);">
                    {patient.get('FirstName', 'N/A')} {patient.get('LastName', 'N/A')}
                </strong>
            </div>
            <div class="patient-field">
                📅 Admit Date: <strong>{admit_date}</strong>
            </div>
            <div class="patient-field">
                🎂 DOB: <strong>{dob_formatted}</strong>
            </div>
            <div class="patient-field">
                🩸 Blood Type: <strong>{blood_type}</strong>
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)

## Dashboard Overview
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h2 style="margin-bottom: 0.5rem;">📊 Dashboard Overview</h2>
    <p style="color: var(--gray-600); margin: 0;">Monitor your dependent patients and key metrics</p>
</div>
""", unsafe_allow_html=True)

## Dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    proxy_id = st.session_state.get('current_proxy_id', 1)
    dependent_patients = get_proxy_patients(proxy_id)
    patient_count = len(dependent_patients) if dependent_patients else 0
    st.markdown(create_metric_card(patient_count, "Dependent Patients", "👥", "primary"), unsafe_allow_html=True)

with col2:
    insurance_count = 0
    if dependent_patients:
        for patient in dependent_patients:
            insurance_info = get_insurance_info(patient.get('PatientID'))
            insurance_count += len(insurance_info) if insurance_info else 0
    
    st.markdown(create_metric_card(insurance_count, "Insurance Policies", "🛡️", "success"), unsafe_allow_html=True)

with col3:
    messages = get_messages(proxy_id)
    message_count = len(messages) if messages else 0
    st.markdown(create_metric_card(message_count, "Unread Messages", "📬", "danger"), unsafe_allow_html=True)

# Add medical divider
st.markdown(create_medical_divider(), unsafe_allow_html=True)

# Patient search and list
st.markdown("""
<div style="margin: 2rem 0;">
    <h3 style="margin-bottom: 1rem;">🔍 Patient Search</h3>
</div>
""", unsafe_allow_html=True)

patient_search = st.text_input(
    "Patient Search", 
    placeholder="Search patients by name...", 
    label_visibility="visible",
    help="Enter patient name to filter the list"
)

st.markdown("""
<div style="margin: 2rem 0;">
    <h3 style="margin-bottom: 1rem;">👥 Dependent Patients</h3>
</div>
""", unsafe_allow_html=True)

if patient_search:
    # Search patients by their names
    filtered_patients = []
    if dependent_patients:
        for patient in dependent_patients:
            full_name = f"{patient.get('FirstName', '')} {patient.get('LastName', '')}".lower()
            if patient_search.lower() in full_name:
                filtered_patients.append(patient)

    if filtered_patients:
        st.markdown(f"""
        <div class="alert-card success">
            <strong>✅ Found {len(filtered_patients)} patients matching '{patient_search}'</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-card warning">
            <strong>⚠️ No patients found matching '{patient_search}'</strong>
        </div>
        """, unsafe_allow_html=True)
        filtered_patients = dependent_patients[:4]  # Show default list
else:
    filtered_patients = dependent_patients[:4] if dependent_patients else []

# Get patient details and render patient cards
if filtered_patients:
    for patient in filtered_patients:
        patient_details = get_patient_details(patient.get('PatientID'))
        render_patient_card(patient_details)
else:
    st.markdown("""
    <div class="medical-card" style="text-align: center; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);">
        <h4 style="color: var(--gray-700); margin-bottom: 0.5rem;">📋 No Patient Data</h4>
        <p style="color: var(--gray-600); margin: 0;">No dependent patient data available at this time.</p>
    </div>
    """, unsafe_allow_html=True)

