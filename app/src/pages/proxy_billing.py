## Proxy Billing - Insurance & Billing Management

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
    page_title="Proxy Billing - Insurance & Billing",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("# 💰 Insurance & Billing Management")
st.write("Manage insurance policies and billing for your dependent patients.")

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

def get_insurance_info(patient_id):
    """Get insurance information for patient"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/patients/{patient_id}/insurance")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to insurance API, using dummy data.")
        return [{"InsuranceProvider": "Blue Cross", "PolicyNumber": "BC123456", "Deductible": 1000.00, "DueDate": "2024-12-31"}]

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

## Billing Overview
st.markdown("## 📊 Billing Overview")

dependent_patients = get_proxy_patients(proxy_id)

if dependent_patients:
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_patients = len(dependent_patients)
        st.metric("Number of Dependents", total_patients)
    
    with col2:
        # Get provider names
        providers = set()
        for p in dependent_patients:
            insurance_info = get_insurance_info(p.get('PatientID'))
            if insurance_info:
                for ins in insurance_info:
                    if isinstance(ins, dict) and 'InsuranceProvider' in ins:
                        providers.add(ins['InsuranceProvider'])
        st.metric("Insurance Providers", len(providers))
    
    with col3:
        # Calculate total deductible safely
        total_deductible = 0
        for p in dependent_patients:
            insurance_info = get_insurance_info(p.get('PatientID'))
            if insurance_info:
                for ins in insurance_info:
                    if isinstance(ins, dict) and 'Deductible' in ins:
                        try:
                            deductible = float(ins['Deductible'])
                            total_deductible += deductible
                        except (ValueError, TypeError):
                            pass
        st.metric("Total Deductible", f"${total_deductible:,.2f}")
    
    st.markdown("---")
    
    ## Insurance Details
    st.markdown("## 🏥 Insurance Details")
    
    for patient in dependent_patients:
        with st.expander(f"📋 {patient.get('FirstName', '')} {patient.get('LastName', '')}", expanded=True):
            insurance_info = get_insurance_info(patient.get('PatientID'))
            
            if insurance_info:
                for insurance in insurance_info:
                    st.markdown(f"""
                    **Provider:** {insurance.get('InsuranceProvider', 'N/A')}
                    **Deductible:** ${insurance.get('Deductible', 'N/A')}
                    **Due Date:** {insurance.get('DueDate', 'N/A')}
                    """)
                    
                    st.divider()
            else:
                st.info("No insurance information available")
                st.divider()
    
else:
    st.info("No dependent patients found for billing information.")
