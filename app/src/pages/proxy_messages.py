## Proxy Messages - Inbox & Alerts

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Proxy Messages - Inbox & Alerts",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded",
)

## Add logo and navigation
SideBarLinks()

st.write("# 📥 Inbox & Alerts")
st.write("View messages and alerts for your dependent patients.")

# API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
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

def get_doctors():
    """Get all doctors for recipient selection"""
    try:
        response = requests.get(f"{API_BASE_URL}/doctor/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_nurses():
    """Get all nurses for recipient selection"""
    try:
        response = requests.get(f"{API_BASE_URL}/nurse/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_message(subject, content, recipient_type, recipient_id, priority, sender_id, sender_role):
    """Create and send a new message"""
    try:
        # Create the message with basic information
        message_data = {
            "Subject": subject,
            "Content": content,
            "PostedBy": sender_id,
            "PostedByRole": sender_role,
            "SenderType": sender_role,
            "ReadStatus": False,
            "Priority": priority,
            "SentTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Actually call the API
        response = requests.post(f"{API_BASE_URL}/message/", json=message_data)
        
        if response.status_code == 201:
            response_data = response.json()
            
            # Get the message ID from response
            message_id = response_data.get('message_id')
            
            if message_id:
                # Link message to recipient based on type
                if recipient_type == "doctor":
                    link_response = requests.post(f"{API_BASE_URL}/message/{message_id}/link_doctor", json={"DoctorID": recipient_id})
                elif recipient_type == "nurse":
                    link_response = requests.post(f"{API_BASE_URL}/message/{message_id}/link_nurse", json={"NurseID": recipient_id})
                elif recipient_type == "patient":
                    link_response = requests.post(f"{API_BASE_URL}/message/{message_id}/link_patient", json={"PatientID": recipient_id})
                
                if link_response.status_code == 200:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    except Exception as e:
        return False

def get_messages(proxy_id):
    """Get messages for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/message/?user_type=proxy&user_id={proxy_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [
            {"MessageID": 1, "Subject": "Appointment Confirmation", "Content": "Your appointment has been confirmed for tomorrow at 2:00 PM", "Priority": "Normal", "From": "Dr. Smith", "Date": "2024-01-20", "Read": False},
            {"MessageID": 2, "Subject": "Insurance Update", "Content": "Your insurance information has been updated in our system", "Priority": "Normal", "From": "Billing Department", "Date": "2024-01-19", "Read": True},
            {"MessageID": 3, "Subject": "Care Plan Review", "Content": "It's time to review and update your care plan", "Priority": "High", "From": "Care Team", "Date": "2024-01-18", "Read": False}
        ]

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

## Inbox Overview
st.markdown("## 📊 Inbox Overview")

messages = get_messages(proxy_id)

# Summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_messages = len(messages)
    st.metric("Total Messages", total_messages)

with col2:
    unread_messages = len([m for m in messages if not m.get('Read', False)])
    st.metric("Unread Messages", unread_messages)

with col3:
    high_priority = len([m for m in messages if m.get('Priority') == 'High'])
    st.metric("High Priority", high_priority)

st.markdown("---")

## Messages Section
st.markdown("## 📧 Messages")

if messages:
    # Display messages
    for message in messages:
        with st.expander(f"📧 {message.get('Subject', 'No Subject')} - {message.get('Date', 'N/A')}"):
            st.markdown(f"**From:** {message.get('From', 'Unknown')}")
            st.markdown(f"**Content:** {message.get('Content', 'No content')}")
            st.markdown(f"**Read:** {'Yes' if message.get('Read') else 'No'}")
            st.markdown(f"**Priority:** {message.get('Priority', 'Normal')}")
else:
    st.info("No messages in your inbox.")

st.markdown("---")

## Compose Message Section
st.markdown("## ✉️ Compose Message")

# Create two columns for inbox and compose
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📥 Inbox")
    
    if not messages:
        st.info("No messages in your inbox.")
    else:
        # Display messages
        for message in messages:
            with st.expander(f"📧 {message.get('Subject', 'No Subject')} - {message.get('Date', 'N/A')}"):
                st.markdown(f"**From:** {message.get('From', 'Unknown')}")
                st.markdown(f"**Content:** {message.get('Content', 'No content')}")
                st.markdown(f"**Read:** {'Yes' if message.get('Read') else 'No'}")
                st.markdown(f"**Priority:** {message.get('Priority', 'Normal')}")

with col2:
    st.markdown("### ✉️ Compose Message")
    
    # Recipient selection outside the form for dynamic updates
    if 'recipient_type' not in st.session_state:
        st.session_state.recipient_type = "doctor"
    
    recipient_type = st.selectbox("Send to:", ["doctor", "nurse"], key="recipient_type_selector")
    
    # Update session state when selection changes
    if st.session_state.recipient_type != recipient_type:
        st.session_state.recipient_type = recipient_type
        st.rerun()
    
    # Show appropriate recipient dropdown based on selection
    recipient_id = None
    
    if st.session_state.recipient_type == "doctor":
        doctors = get_doctors()
        if doctors:
            recipient_options = {f"Dr. {d.get('LastName', '')} ({d.get('Specialty', '')})": d.get('DoctorID') for d in doctors}
            recipient = st.selectbox("Select Doctor:", list(recipient_options.keys()), key="doctor_selector")
            recipient_id = recipient_options[recipient] if recipient else None
        else:
            st.warning("No doctors available")
            recipient_id = None
            
    elif st.session_state.recipient_type == "nurse":
        nurses = get_nurses()
        if nurses:
            recipient_options = {f"{n.get('FirstName', '')} {n.get('LastName', '')}": n.get('NurseID') for n in nurses}
            recipient = st.selectbox("Select Nurse:", list(recipient_options.keys()), key="nurse_selector")
            recipient_id = recipient_options[recipient] if recipient else None
        else:
            st.warning("No nurses available")
            recipient_id = None
    
    # Message composition form
    with st.form("compose_message"):
        subject = st.text_input("Subject", placeholder="Enter message subject...", key="subject_input")
        content = st.text_area("Message", placeholder="Type your message here...", height=150, key="content_input")
        
        # Priority selection
        priority = st.selectbox("Priority:", ["Normal", "High", "Urgent"], key="priority_input")
        
        # Send button
        submitted = st.form_submit_button("📤 Send Message", type="primary", use_container_width=True)
    
    # Handle form submission outside the form
    if submitted:
        # Get form data from session state
        subject = st.session_state.get("subject_input", "")
        content = st.session_state.get("content_input", "")
        priority = st.session_state.get("priority_input", "Normal")
        
        if subject and content and recipient_id:
            st.success("✅ Message sent successfully!")
            
            # Call create_message function
            create_message(subject, content, st.session_state.recipient_type, recipient_id, priority, proxy_id, "Proxy")
            
        else:
            st.warning("Please fill in all required fields.")
