## Nurse Messages - Inbox & Message Creation

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.styles import apply_page_styling, create_medical_divider

## Apply medical theme and styling
apply_page_styling()

## Add logo and navigation
SideBarLinks()

# Medical-themed header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">📥 Nurse Inbox & Messages</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        View messages and create new ones
    </p>
</div>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
def get_nurses():
    """Get all nurses from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/nurse/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to nurses API, using dummy data.")
        return [{"NurseID": 1, "FirstName": "Nic", "LastName": "Nevin"}]

def get_nurse_by_name(first_name, last_name):
    """Get nurse information by name"""
    try:
        response = requests.get(f"{API_BASE_URL}/nurse/")
        if response.status_code == 200:
            nurses = response.json()
            for nurse in nurses:
                if nurse.get('FirstName') == first_name and nurse.get('LastName') == last_name:
                    return nurse
        return None
    except:
        st.warning("Could not connect to nurse API, using dummy data.")
        return {"NurseID": 1, "FirstName": "Nic", "LastName": "Nevin"}

def get_doctors():
    """Get all doctors for recipient selection"""
    try:
        response = requests.get(f"{API_BASE_URL}/doctor/")
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

def get_messages(nurse_id):
    """Get messages for specific nurse"""
    try:
        response = requests.get(f"{API_BASE_URL}/message/?user_type=nurse&user_id={nurse_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [
            {"MessageID": 1, "Subject": "Patient Update", "Content": "Patient condition improved", "Priority": "Normal", "SentTime": "2024-01-15 10:30:00", "SenderType": "Doctor", "PostedBy": 1, "ReadStatus": False},
            {"MessageID": 2, "Subject": "Schedule Change", "Content": "Your shift has been changed to 3-11 PM", "Priority": "High", "SentTime": "2024-01-16 08:00:00", "SenderType": "System", "PostedBy": 1, "ReadStatus": True}
        ]

## Get nurse information
# Try to get nurse by name first, then fall back to first nurse
nurse_info = get_nurse_by_name("Nic", "Nevin")
if nurse_info:
    nurse_id = nurse_info.get('NurseID', 1)
    nurse_name = f"{nurse_info.get('FirstName', 'Nic')} {nurse_info.get('LastName', 'Nevin')}"
else:
    # Fallback to first nurse if name lookup fails
    nurses = get_nurses()
    if nurses:
        current_nurse = nurses[0]
        nurse_id = current_nurse.get('NurseID', 1)
        nurse_name = f"{current_nurse.get('FirstName', 'Nic')} {current_nurse.get('LastName', 'Nevin')}"
    else:
        nurse_id = 1
        nurse_name = "Nic Nevin"

## Welcome message
st.markdown(f"### Welcome, {nurse_name}")

st.markdown("---")

## Inbox Overview
st.markdown("## 📊 Inbox Overview")

messages = get_messages(nurse_id)

# Summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_messages = len(messages)
    st.metric("Total Messages", total_messages)

with col2:
    unread_messages = len([m for m in messages if not m.get('ReadStatus', False)])
    st.metric("Unread Messages", unread_messages)

with col3:
    high_priority = len([m for m in messages if m.get('Priority') == 'High'])
    st.metric("High Priority", high_priority)

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
            with st.expander(f"📧 {message.get('Subject', 'No Subject')} - {message.get('SentTime', 'N/A')}"):
                st.markdown(f"**From:** {message.get('SenderType', 'Unknown')} {message.get('PostedBy', 'N/A')}")
                st.markdown(f"**Content:** {message.get('Content', 'No content')}")
                st.markdown(f"**Read:** {'Yes' if message.get('ReadStatus') else 'No'}")
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
            # Filter out current nurse
            other_doctors = [d for d in doctors if d.get('DoctorID') != nurse_id]
            if other_doctors:
                recipient_options = {f"Dr. {d.get('LastName', '')} ({d.get('Specialty', '')})": d.get('DoctorID') for d in other_doctors}
                recipient = st.selectbox("Select Doctor:", list(recipient_options.keys()), key="doctor_selector")
                recipient_id = recipient_options[recipient] if recipient else None
            else:
                st.warning("No other doctors available")
                recipient_id = None
        else:
            st.warning("No doctors available")
            recipient_id = None
            
    elif st.session_state.recipient_type == "nurse":
        nurses = get_nurses()
        if nurses:
            # Filter out current nurse
            other_nurses = [n for n in nurses if n.get('NurseID') != nurse_id]
            if other_nurses:
                recipient_options = {f"{n.get('FirstName', '')} {n.get('LastName', '')}": n.get('NurseID') for n in other_nurses}
                recipient = st.selectbox("Select Nurse:", list(recipient_options.keys()), key="nurse_selector")
                recipient_id = recipient_options[recipient] if recipient else None
            else:
                st.warning("No other nurses available")
                recipient_id = None
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
            create_message(subject, content, st.session_state.recipient_type, recipient_id, priority, nurse_id, "Nurse")
            
        else:
            st.warning("Please fill in all required fields.")


