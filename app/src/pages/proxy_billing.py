## Proxy Billing - Insurance & Billing Management

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Page config - MUST be first Streamlit command
from modules.styles import apply_page_styling, create_metric_card, create_medical_divider

## Apply medical theme and styling
apply_page_styling()

## Add logo and navigation
SideBarLinks()

# Medical-themed header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">💰 Insurance & Billing Management</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        Manage insurance policies and billing for your dependent patients
    </p>
</div>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
def get_proxies():
    """Get all proxies"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxy/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to proxies API, using dummy data.")
        return [{"ProxyID": 1, "FirstName": "Nina", "LastName": "Pesci", "Relationship": "Child"}]

def get_proxy_by_name(first_name, last_name):
    """Get proxy information by name"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxy/name/{first_name}/{last_name}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        st.warning("Could not connect to proxy API, using dummy data.")
        return {"ProxyID": 1, "FirstName": "Nina", "LastName": "Pesci", "Relationship": "Child"}

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

def get_insurance_info(patient_id):
    """Get insurance information for patient"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/insurance")
        if response.status_code == 200:
            insurance_data = response.json()
            # Backend returns a single insurance record, wrap it in a list for consistency
            if insurance_data and isinstance(insurance_data, dict):
                return [insurance_data]
            return []
        elif response.status_code == 404:
            # No insurance found for this patient
            return []
        else:
            st.warning(f"Insurance API returned status {response.status_code}")
            return []
    except Exception as e:
        st.warning(f"Could not connect to insurance API: {str(e)}")
        # Return dummy data for testing
        return [{"InsuranceProvider": "Blue Cross", "PolicyNumber": "BC123456", "Deductible": 1000.00, "DueDate": "2024-12-31"}]

## Get proxy information
# Try to get proxy by name first, then fall back to first proxy
proxy_info = get_proxy_by_name("Nina", "Pesci")
if proxy_info:
    proxy_id = proxy_info.get('ProxyID', 1)
    proxy_name = f"{proxy_info.get('FirstName', 'Nina')} {proxy_info.get('LastName', 'Pesci')}"
else:
    # Fallback to first proxy if name lookup fails
    proxies = get_proxies()
    if proxies:
        current_proxy = proxies[0]
        proxy_id = current_proxy.get('ProxyID', 1)
        proxy_name = f"{current_proxy.get('FirstName', 'Nina')} {current_proxy.get('LastName', 'Pesci')}"
    else:
        proxy_id = 1
        proxy_name = "Nina Pesci"

## Welcome message
st.markdown(f"### Welcome, {proxy_name}")

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
                    # Check if insurance is a dictionary with the expected structure
                    if isinstance(insurance, dict) and 'InsuranceProvider' in insurance:
                        st.markdown(f"""
                        **Provider:** {insurance.get('InsuranceProvider', 'N/A')}
                        **Deductible:** ${insurance.get('Deductible', 'N/A')}
                        **Due Date:** {insurance.get('DueDate', 'N/A')}
                        """)
                    else:
                        st.warning("Invalid insurance data format")
                    
                    st.divider()
            else:
                st.info("No insurance information available")
                st.divider()
    
else:
    st.info("No dependent patients found for billing information.")
