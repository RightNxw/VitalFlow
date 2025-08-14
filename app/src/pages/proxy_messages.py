## Proxy Messages - Inbox & Message Creation

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
    <h1 style="margin-bottom: 0.5rem;">📬 Proxy Messages & Communications</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        View and manage messages for your dependent patient
    </p>
</div>
""", unsafe_allow_html=True)

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

def get_patients():
    """Get all patients for recipient selection"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/")
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
                    link_response = requests.post(f"{API_BASE_URL}/message/messages/{message_id}/link_doctor", json={"DoctorID": recipient_id})
                elif recipient_type == "nurse":
                    link_response = requests.post(f"{API_BASE_URL}/message/messages/{message_id}/link_nurse", json={"NurseID": recipient_id})
                elif recipient_type == "patient":
                    link_response = requests.post(f"{API_BASE_URL}/message/messages/{message_id}/link_patient", json={"PatientID": recipient_id})
                
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

def delete_message(message_id):
    """Delete a message (acknowledge it)"""
    try:
        response = requests.delete(f"{API_BASE_URL}/message/messages/{message_id}")
        if response.status_code == 200:
            # Store success message in session state
            st.session_state['delete_success'] = f"Message {message_id} acknowledged and deleted!"
            return True
        elif response.status_code == 404:
            st.info("No data found for this message")
            return False
        else:
            st.error(f"Failed to delete message: {response.status_code}")
            return False
    except:
        st.error("Connection error - please try again")
        return False

def get_messages(proxy_id):
    """Get messages for specific proxy (via their associated patient)"""
    try:
        # First get the proxy's associated patient ID
        proxy_response = requests.get(f"{API_BASE_URL}/proxy/{proxy_id}")
        if proxy_response.status_code == 200:
            proxy_data = proxy_response.json()
            patient_id = proxy_data.get('PatientID')
            
            if patient_id:
                # Get messages for the associated patient
                response = requests.get(f"{API_BASE_URL}/message/?user_type=patient&user_id={patient_id}")
                if response.status_code == 200:
                    return response.json()
        
        # Fallback to dummy data if anything fails
        return [
            {"MessageID": 1, "Subject": "Appointment Confirmation", "Content": "Your appointment has been confirmed for tomorrow at 2:00 PM", "Priority": "Normal", "SentTime": "2024-01-20 10:00:00", "SenderType": "Dr. Smith", "PostedBy": 1, "ReadStatus": False},
            {"MessageID": 2, "Subject": "Insurance Update", "Content": "Your insurance information has been updated in our system", "Priority": "Normal", "SentTime": "2024-01-19 14:30:00", "SenderType": "Billing Department", "PostedBy": 2, "ReadStatus": True},
            {"MessageID": 3, "Subject": "Care Plan Review", "Content": "It's time to review and update your care plan", "Priority": "High", "SentTime": "2024-01-18 09:15:00", "SenderType": "Care Team", "PostedBy": 3, "ReadStatus": False}
        ]
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [
            {"MessageID": 1, "Subject": "Appointment Confirmation", "Content": "Your appointment has been confirmed for tomorrow at 2:00 PM", "Priority": "Normal", "SentTime": "2024-01-20 10:00:00", "SenderType": "Dr. Smith", "PostedBy": 1, "ReadStatus": False},
            {"MessageID": 2, "Subject": "Insurance Update", "Content": "Your insurance information has been updated in our system", "Priority": "Normal", "SentTime": "2024-01-19 14:30:00", "SenderType": "Billing Department", "PostedBy": 2, "ReadStatus": True},
            {"MessageID": 3, "Subject": "Care Plan Review", "Content": "It's time to review and update your care plan", "Priority": "High", "SentTime": "2024-01-18 09:15:00", "SenderType": "Care Team", "PostedBy": 3, "ReadStatus": False}
        ]

## Get proxy information
# Try to get proxy by name first, then fall back to first proxy
proxy_info = get_proxy_by_name("Nina", "Pesci")
if proxy_info:
    proxy_id = proxy_info.get('ProxyID', 1)
    proxy_name = f"{proxy_info.get('FirstName', 'Nina')} {proxy_info.get('LastName', 'Pesci')}"
    relationship = proxy_info.get('Relationship', 'Unknown')
else:
    # Fallback to first proxy if name lookup fails
    proxies = get_proxies()
    if proxies:
        current_proxy = proxies[0]
        proxy_id = current_proxy.get('ProxyID', 1)
        proxy_name = f"{current_proxy.get('FirstName', 'Nina')} {current_proxy.get('LastName', 'Nina')}"
        relationship = current_proxy.get('Relationship', 'Unknown')
    else:
        proxy_id = 1
        proxy_name = "Nina Pesci"
        relationship = "Unknown"

## Welcome message
st.markdown(f"### Welcome, {proxy_name} ({relationship})")

st.markdown("---")

## Get messages for current proxy's patient
messages = get_messages(proxy_id)

# Display success messages if they exist
if 'delete_success' in st.session_state:
    st.success(st.session_state['delete_success'])
    # Clear the message after displaying
    del st.session_state['delete_success']

if 'message_sent_success' in st.session_state:
    st.success("✅ Message sent successfully!")
    # Clear the message after displaying
    del st.session_state['message_sent_success']

# Create two columns for inbox and compose
col1, col2 = st.columns([1.5, 1])  # Give compose section more space

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
                
                # Add acknowledge/delete button
                col1_inner, col2_inner = st.columns([3, 1])
                with col1_inner:
                    st.markdown(f"**Message ID:** {message.get('MessageID', 'N/A')}")
                with col2_inner:
                    if st.button("✅ Acknowledge", key=f"ack_{message.get('MessageID')}", use_container_width=True):
                        if delete_message(message.get('MessageID')):
                            st.rerun()
                        else:
                            st.error("Failed to delete message")

with col2:
    st.markdown("### ✉️ Compose Message")
    
    # Recipient selection outside the form for dynamic updates
    if 'recipient_type' not in st.session_state:
        st.session_state.recipient_type = "doctor"
    
    recipient_type = st.selectbox("Send to:", ["doctor", "nurse", "patient"], key="recipient_type_selector")
    
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
            
    elif st.session_state.recipient_type == "patient":
        patients = get_patients()
        if patients:
            recipient_options = {f"{p.get('FirstName', '')} {p.get('LastName', '')} (ID: {p.get('PatientID', '')})": p.get('PatientID') for p in patients}
            recipient = st.selectbox("Select Patient:", list(recipient_options.keys()), key="patient_selector")
            recipient_id = recipient_options[recipient] if recipient else None
        else:
            st.warning("No patients available")
            recipient_id = None
    
    # Message composition form
    with st.form("compose_message"):
        subject = st.text_input("Subject", placeholder="Enter message subject...", key="subject_input")
        content = st.text_area("Message", placeholder="Type your message here...", height=120, key="content_input")
        
        # Priority selection
        priority = st.selectbox("Priority:", ["Normal", "High", "Urgent"], key="priority_input")
        
        # Send button
        submitted = st.form_submit_button("📤 Send Message", type="primary", use_container_width=True)
    
    # Handle form submission outside the form
    if submitted:
        if subject and content and recipient_id:
            # Call create_message function
            if create_message(subject, content, st.session_state.recipient_type, recipient_id, priority, proxy_id, "Proxy"):
                # Store success message in session state
                st.session_state['message_sent_success'] = True
                # Rerun to refresh the page and clear form
                st.rerun()
            else:
                st.error("❌ Failed to send message. Please try again.")
        else:
            st.warning("Please fill in all required fields.")
