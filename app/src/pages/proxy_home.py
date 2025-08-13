## Proxy Home Page

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
    page_title="Proxy Home",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("# Proxy Home")
st.write("Manage patient information and billing for your dependents.")

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

def get_insurance_info(patient_id):
    """Get insurance information for patient"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/insurance")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to insurance API, using dummy data.")
        return [{"InsuranceProvider": "Blue Cross", "PolicyNumber": "BC123456", "Deductible": 1000.00}]

def get_alerts(proxy_id):
    """Get alerts for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/alerts?user_type=proxy&user_id={proxy_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [{"AlertID": 1, "Title": "Medication Refill", "Description": "Patient needs medication refill", "Severity": "Medium"}]

def get_messages(proxy_id):
    """Get messages for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/messages?user_type=proxy&user_id={proxy_id}")
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
    st.markdown(f"### Welcome, {proxy_name}")
else:
    st.markdown("### Welcome, Nina Pesci")

## Search bar
top_left, top_spacer, top_right = st.columns([6, 1, 1])
with top_left:
    global_search = st.text_input("Search", placeholder="Search patients, insurance, billing...", label_visibility="visible")

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

    st.markdown(card_html, unsafe_allow_html=True)

## Dashboard Overview
st.markdown("### Dashboard Overview")

## Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    proxy_id = st.session_state.get('current_proxy_id', 1)
    dependent_patients = get_proxy_patients(proxy_id)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(dependent_patients) if dependent_patients else 0}</div>
            <div class="metric-label">Dependent Patients</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    insurance_count = 0
    if dependent_patients:
        for patient in dependent_patients:
            insurance_info = get_insurance_info(patient.get('PatientID'))
            insurance_count += len(insurance_info) if insurance_info else 0
    
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{insurance_count}</div>
            <div class="metric-label">Insurance Policies</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    alerts = get_alerts(proxy_id)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(alerts) if alerts else 0}</div>
            <div class="metric-label">Active Alerts</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    messages = get_messages(proxy_id)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(messages) if messages else 0}</div>
            <div class="metric-label">Unread Messages</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Patient search and list
patient_search = st.text_input("Patient Search", placeholder="Search patients by name...", label_visibility="visible")

st.markdown("### Dependent Patients")

if patient_search:
    # Search patients by their names
    filtered_patients = []
    if dependent_patients:
        for patient in dependent_patients:
            full_name = f"{patient.get('FirstName', '')} {patient.get('LastName', '')}".lower()
            if patient_search.lower() in full_name:
                filtered_patients.append(patient)

    if filtered_patients:
        st.info(f"Found {len(filtered_patients)} patients matching '{patient_search}'")
    else:
        st.warning(f"No patients found matching '{patient_search}'")
        filtered_patients = dependent_patients[:4]  # Show default list
else:
    filtered_patients = dependent_patients[:4] if dependent_patients else []

# Get patient details and render patient cards
if filtered_patients:
    for patient in filtered_patients:
        patient_details = get_patient_details(patient.get('PatientID'))
        render_patient_card(patient_details)
else:
    st.info("No dependent patient data available.")

