## Patient Billing Page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Patient Billing",
    page_icon="💰",
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
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        st.error("Could not connect to patient API")
        return None

def get_patient_insurance(patient_id):
    """Get patient's insurance information"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/insurance")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        st.warning("Could not connect to insurance API")
        return None

def get_patient_visit(patient_id):
    """Get patient's current visit from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/visit")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_patient_condition(patient_id):
    """Get patient's condition from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/condition")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

## Main page
st.markdown("# 💰 Patient Billing & Insurance")

# Get current patient ID from session state
patient_id = st.session_state.get('current_patient_id', 1)
patient_info = get_patient_info(patient_id)

if not patient_info:
    st.error("Could not load patient information")
    st.stop()

patient_name = f"{patient_info.get('FirstName', 'Unknown')} {patient_info.get('LastName', 'Unknown')}"

# Get insurance information
insurance_info = get_patient_insurance(patient_id)

# Get visit information for billing context
visit_info = get_patient_visit(patient_id)

# Get condition information for billing context
condition_info = get_patient_condition(patient_id)

# Billing Overview
st.markdown("### 📊 Billing Overview")

col1, col2, col3 = st.columns(3)

with col1:
    if insurance_info:
        st.metric("Insurance Provider", insurance_info.get('InsuranceProvider', 'N/A'))
    else:
        st.metric("Insurance Provider", "No Insurance")

with col2:
    if insurance_info and insurance_info.get('Deductible'):
        try:
            # Convert to float and format properly
            deductible = float(insurance_info.get('Deductible', 0))
            st.metric("Deductible", f"${deductible:,.2f}")
        except (ValueError, TypeError):
            st.metric("Deductible", insurance_info.get('Deductible', 'N/A'))
    else:
        st.metric("Deductible", "$0.00")

with col3:
    if visit_info:
        st.metric("Current Visit", "Active")
    else:
        st.metric("Current Visit", "None")

st.markdown("---")

# Insurance Details
st.markdown("### 🏥 Insurance Details")

if insurance_info:
    with st.expander("Insurance Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Provider:** {insurance_info.get('InsuranceProvider', 'N/A')}
            **Policy Number:** {insurance_info.get('PolicyNumber', 'N/A')}
            **Deductible:** {insurance_info.get('Deductible', 'N/A')}
            """)
        
        with col2:
            st.markdown(f"""
            **Due Date:** {insurance_info.get('DueDate', 'N/A')}
            **Coverage Status:** Active
            """)
else:
    st.info("No insurance information available for this patient")

st.markdown("---")

# Visit Information for Billing Context
st.markdown("### 🏥 Visit Information")

if visit_info:
    with st.expander("Current Visit Details", expanded=True):
        st.markdown(f"""
        **Admit Reason:** {visit_info.get('AdmitReason', 'N/A')}
        **Appointment Date:** {visit_info.get('AppointmentDate', 'N/A')}
        **Next Visit Date:** {visit_info.get('NextVisitDate', 'N/A')}
        """)
else:
    st.info("No current visit information available")

st.markdown("---")

# Condition Information for Billing Context
st.markdown("### 🏥 Medical Condition")

if condition_info:
    with st.expander("Current Condition Details", expanded=True):
        st.markdown(f"""
        **Description:** {condition_info.get('Description', 'N/A')}
        **Treatment:** {condition_info.get('Treatment', 'N/A')}
        """)
else:
    st.info("No condition information available")

st.markdown("---")

# Billing Actions
st.markdown("### 💳 Billing Actions")

col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Generate Bill", use_container_width=True):
        st.info("Billing system integration would be implemented here")
        if visit_info and insurance_info:
            st.success(f"Bill generated for visit: {visit_info.get('AdmitReason', 'N/A')}")
            st.info(f"Insurance: {insurance_info.get('InsuranceProvider', 'N/A')}")
            try:
                deductible = float(insurance_info.get('Deductible', 0))
                st.info(f"Deductible remaining: ${deductible:,.2f}")
            except (ValueError, TypeError):
                st.info(f"Deductible remaining: {insurance_info.get('Deductible', 'N/A')}")

with col2:
    if st.button("📊 View Payment History", use_container_width=True):
        st.info("Payment history would be displayed here")
        st.info("This would show all previous payments and outstanding balances")

st.markdown("---")

# Cost Breakdown (if visit exists)
if visit_info:
    st.markdown("### 💵 Estimated Cost Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Consultation Fee", "$150.00")
    
    with col2:
        st.metric("Lab Tests", "$75.00")
    
    with col3:
        st.metric("Total Estimated", "$225.00")
    
    if insurance_info:
        st.info(f"**Insurance Coverage:** {insurance_info.get('InsuranceProvider', 'N/A')} will cover 80% after deductible")
        try:
            deductible = float(insurance_info.get('Deductible', 0))
            st.info(f"**Your Responsibility:** ${deductible:,.2f} deductible + 20% of remaining costs")
        except (ValueError, TypeError):
            st.info(f"**Your Responsibility:** {insurance_info.get('Deductible', 'N/A')} deductible + 20% of remaining costs")
else:
    st.info("No active visit to calculate costs")
