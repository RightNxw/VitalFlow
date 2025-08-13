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
        return [{"InsuranceProvider": "Blue Cross", "PolicyNumber": "BC123456", "Deductible": 1000.00, "CoverageType": "Family", "GroupNumber": "GRP789"}]

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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = len(dependent_patients)
        st.metric("Total Dependents", total_patients)
    
    with col2:
        total_insurance = sum(len(get_insurance_info(p.get('PatientID'))) for p in dependent_patients)
        st.metric("Insurance Policies", total_insurance)
    
    with col3:
        total_deductible = sum(
            sum(ins.get('Deductible', 0) for ins in get_insurance_info(p.get('PatientID')))
            for p in dependent_patients
        )
        st.metric("Total Deductible", f"${total_deductible:,.2f}")
    
    with col4:
        outstanding_balance = 0.00  # This would come from billing API
        st.metric("Outstanding Balance", f"${outstanding_balance:,.2f}")
    
    st.markdown("---")
    
    ## Individual Patient Billing
    st.markdown("## 🏥 Patient Insurance & Billing Details")
    
    for patient in dependent_patients:
        with st.expander(f"📋 {patient.get('FirstName', '')} {patient.get('LastName', '')} - Insurance & Billing", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏥 Insurance Details")
                insurance_info = get_insurance_info(patient.get('PatientID'))
                
                if insurance_info:
                    for insurance in insurance_info:
                        st.markdown(f"""
                        **Provider:** {insurance.get('InsuranceProvider', 'N/A')}
                        **Policy Number:** {insurance.get('PolicyNumber', 'N/A')}
                        **Deductible:** ${insurance.get('Deductible', 'N/A')}
                        **Coverage Type:** {insurance.get('CoverageType', 'N/A')}
                        **Group Number:** {insurance.get('GroupNumber', 'N/A')}
                        """)
                        
                        # Insurance actions
                        if st.button("📄 View Policy", key=f"policy_{patient.get('PatientID')}_{insurance.get('PolicyNumber', '')}", use_container_width=True):
                            st.info(f"Policy details for {insurance.get('InsuranceProvider', 'Insurance')}")
                        
                        if st.button("📞 Contact Provider", key=f"contact_{patient.get('PatientID')}_{insurance.get('PolicyNumber', '')}", use_container_width=True):
                            st.info(f"Contact {insurance.get('InsuranceProvider', 'Insurance Provider')}")
                else:
                    st.info("No insurance information available")
            
            with col2:
                st.markdown("### 💳 Billing Summary")
                st.markdown(f"""
                **Patient:** {patient.get('FirstName', '')} {patient.get('LastName', '')}
                **Patient ID:** {patient.get('PatientID', 'N/A')}
                **Last Billing Date:** {datetime.now().strftime('%m/%d/%Y')}
                **Outstanding Balance:** $0.00
                **Next Payment Due:** N/A
                **Payment Method:** Credit Card on File
                """)
                
                # Billing actions
                if st.button("📄 Download Statement", key=f"download_{patient.get('PatientID')}", use_container_width=True):
                    st.info("Statement download initiated")
                
                if st.button("💳 Make Payment", key=f"payment_{patient.get('PatientID')}", use_container_width=True):
                    st.info("Payment portal would open here")
                
                if st.button("📧 Request Billing Info", key=f"request_{patient.get('PatientID')}", use_container_width=True):
                    st.info("Billing information request sent")
            
            st.divider()
    
    ## Payment History
    st.markdown("---")
    st.markdown("## 📈 Payment History")
    
    # Dummy payment history data
    payment_history = [
        {"Date": "2024-01-15", "Patient": "Joe Pesci", "Amount": 150.00, "Status": "Paid"},
        {"Date": "2024-01-10", "Patient": "Maria Pesci", "Amount": 200.00, "Status": "Paid"},
        {"Date": "2024-01-05", "Patient": "Joe Pesci", "Amount": 75.00, "Status": "Paid"}
    ]
    
    if payment_history:
        df = pd.DataFrame(payment_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No payment history available")
    
else:
    st.info("No dependent patients found for billing information.")
