## Patient Inbox Page

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

def get_patient_messages(patient_id):
    """Get messages for specific patient"""
    try:
        response = requests.get(f"{API_BASE_URL}/message/?user_type=patient&user_id={patient_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ API Error: {response.status_code}")
            return []
    except Exception as e:
        st.warning("Could not connect to messages API, using dummy data.")
        return [
            {
                "MessageID": 1, 
                "Subject": "Appointment Reminder", 
                "Content": "Your annual physical examination is scheduled for January 15th, 2025 at 9:00 AM.", 
                "Priority": "Normal", 
                "SentTime": "2024-12-15 10:30:00", 
                "SenderType": "Nurse", 
                "PostedBy": 1, 
                "ReadStatus": False
            },
            {
                "MessageID": 2, 
                "Subject": "Lab Results Available", 
                "Content": "Your recent lab results are now available in your patient portal. All values are within normal range.", 
                "Priority": "Normal", 
                "SentTime": "2024-12-10 14:15:00", 
                "SenderType": "Doctor", 
                "PostedBy": 2, 
                "ReadStatus": True
            }
        ]

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
                    link_response = requests.post(f"{API_BASE_URL}/message/messages/{message_id}/link_doctor", json={"DoctorID": recipient_id})
                elif recipient_type == "nurse":
                    link_response = requests.post(f"{API_BASE_URL}/message/messages/{message_id}/link_nurse", json={"NurseID": recipient_id})
                
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

## Main page
# Medical-themed header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">📬 Patient Messages & Communications</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        View and manage your messages
    </p>
</div>
""", unsafe_allow_html=True)

# Display success messages if they exist
if 'delete_success' in st.session_state:
    st.success(st.session_state['delete_success'])
    # Clear the message after displaying
    del st.session_state['delete_success']

if 'message_sent_success' in st.session_state:
    st.success("✅ Message sent successfully!")
    # Clear the message after displaying
    del st.session_state['message_sent_success']

# Get current patient ID from session state
patient_id = st.session_state.get('current_patient_id', 1)
patient_info = get_patient_info(patient_id)

if not patient_info:
    st.error("Could not load patient information")
    st.stop()

patient_name = f"{patient_info.get('FirstName', 'Unknown')} {patient_info.get('LastName', 'Unknown')}"

# Get messages for this patient
messages = get_patient_messages(patient_id)

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
        if subject and content and recipient_id:
            # Call create_message function
            if create_message(subject, content, st.session_state.recipient_type, recipient_id, priority, patient_id, "Patient"):
                # Store success message in session state
                st.session_state['message_sent_success'] = True
                # Rerun to refresh the page and clear form
                st.rerun()
            else:
                st.error("❌ Failed to send message. Please try again.")
        else:
            st.warning("Please fill in all required fields.")

# Message Statistics
st.markdown(create_medical_divider(), unsafe_allow_html=True)
st.markdown("### 📊 Message Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_messages = len(messages)
    st.metric("Total Messages", total_messages)

with col2:
    unread_count = sum(1 for msg in messages if not msg.get('ReadStatus', False))
    st.metric("Unread Messages", unread_count)

with col3:
    high_priority = sum(1 for msg in messages if msg.get('Priority') == 'High')
    st.metric("High Priority", high_priority)

with col4:
    urgent_count = sum(1 for msg in messages if msg.get('Priority') == 'Urgent')
    st.metric("Urgent", urgent_count)


