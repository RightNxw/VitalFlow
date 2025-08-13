import logging
import streamlit as st
import requests
import json
from datetime import datetime
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# Set up the page
st.set_page_config(layout="wide")

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Check if user is authenticated
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Please log in to access the messaging system.")
    st.stop()

# Get user info from session state
user_role = st.session_state.get("role", "unknown")
user_first_name = st.session_state.get("first_name", "User")

# Page header
st.title("📧 Universal Messaging System")
st.markdown(f"**Welcome, {user_role.upper()}. {user_first_name}**")

# API base URL - adjust based on your setup
API_BASE_URL = "http://web-api:4000"

# Helper functions
def get_user_messages(user_type, user_id):
    """Fetch messages for the current user"""
    try:
        response = requests.get(f"{API_BASE_URL}/messages?user_type={user_type}&user_id={user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch messages: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching messages: {str(e)}")
        return []

def send_message(message_data):
    """Send a new message"""
    try:
        response = requests.post(f"{API_BASE_URL}/messages", json=message_data)
        if response.status_code == 201:
            return True, "Message sent successfully!"
        else:
            return False, f"Failed to send message: {response.status_code}"
    except Exception as e:
        return False, f"Error sending message: {str(e)}"

def get_recipients():
    """Get list of potential recipients based on user role"""
    try:
        # Get doctors
        doctors_response = requests.get(f"{API_BASE_URL}/doctors")
        doctors = doctors_response.json() if doctors_response.status_code == 200 else []
        
        # Get nurses
        nurses_response = requests.get(f"{API_BASE_URL}/nurses")
        nurses = nurses_response.json() if nurses_response.status_code == 200 else []
        
        # Get patients
        patients_response = requests.get(f"{API_BASE_URL}/patient/patients")
        patients = patients_response.json() if patients_response.status_code == 200 else []
        
        return doctors, nurses, patients
    except Exception as e:
        st.error(f"Error fetching recipients: {str(e)}")
        return [], [], []

# Main layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### 🔍 Search")
    search_query = st.text_input("Search messages", placeholder="Enter search term...")
    
    st.markdown("### 🏥 Hospital")
    hospital_options = ["General Hospital", "Emergency Center", "Specialty Clinic"]
    selected_hospital = st.selectbox("Select Hospital", hospital_options, index=0)

with col2:
    # New Message Section
    st.markdown("### ✉️ New Message")
    
    with st.form("new_message_form"):
        col_title, col_recipient = st.columns([2, 1])
        
        with col_title:
            message_title = st.text_input("ENTER TITLE", placeholder="Message subject...")
        
        with col_recipient:
            # Get recipients based on user role
            doctors, nurses, patients = get_recipients()
            
            recipient_options = []
            if user_role == "doctor":
                recipient_options.extend([f"nurse_{n['NurseID']}" for n in nurses])
                recipient_options.extend([f"patient_{p['PatientID']}" for p in patients])
            elif user_role == "nurse":
                recipient_options.extend([f"doctor_{d['DoctorID']}" for d in doctors])
                recipient_options.extend([f"patient_{p['PatientID']}" for p in patients])
            elif user_role == "patient":
                recipient_options.extend([f"doctor_{d['DoctorID']}" for d in doctors])
                recipient_options.extend([f"nurse_{n['NurseID']}" for n in nurses])
            else:
                # For admin or other roles, show all
                recipient_options.extend([f"doctor_{d['DoctorID']}" for d in doctors])
                recipient_options.extend([f"nurse_{n['NurseID']}" for n in nurses])
                recipient_options.extend([f"patient_{p['PatientID']}" for p in patients])
            
            selected_recipient = st.selectbox("SEND TO", recipient_options, 
                                           format_func=lambda x: x.replace("_", " ").title())
        
        message_content = st.text_area("ENTER MESSAGE", placeholder="Type your message here...", height=150)
        
        col_send, col_urgency = st.columns([1, 1])
        with col_send:
            send_button = st.form_submit_button("SEND", type="primary", use_container_width=True)
        
        with col_urgency:
            urgency_level = st.selectbox("Urgency Level", [1, 2, 3, 4, 5], 
                                       format_func=lambda x: f"Level {x} - {'Low' if x <= 2 else 'Medium' if x <= 4 else 'High'}")
        
        if send_button and message_title and message_content and selected_recipient:
            # Prepare message data
            recipient_type, recipient_id = selected_recipient.split("_")
            
            message_data = {
                "MessageTitle": message_title,
                "Message": message_content,
                "PostedBy": 1,  # This should be the actual user ID
                "PostedByRole": user_role,
                "RecipientType": recipient_type,
                "RecipientID": int(recipient_id)
            }
            
            success, message = send_message(message_data)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

# All Messages Section
st.markdown("### 📬 All Messages")

# Get messages for current user
user_id = 1  # This should be the actual user ID from session
messages = get_user_messages(user_role, user_id)

if messages:
    # Filter messages based on search query
    if search_query:
        filtered_messages = [
            msg for msg in messages 
            if search_query.lower() in msg.get('Message', '').lower() or 
               search_query.lower() in msg.get('MessageTitle', '').lower()
        ]
    else:
        filtered_messages = messages
    
    # Display messages
    for i, message in enumerate(filtered_messages):
        with st.container():
            col_msg, col_info = st.columns([3, 1])
            
            with col_msg:
                st.markdown(f"**{message.get('MessageTitle', 'No Title')}**")
                st.write(message.get('Message', 'No content'))
            
            with col_info:
                # Determine if message was sent to current user or by current user
                if message.get('PostedByRole') == user_role:
                    st.markdown("**SENT BY YOU**")
                else:
                    st.markdown("**SENT TO YOU**")
                
                # Format timestamp
                sent_time = message.get('SentTime', '')
                if sent_time:
                    try:
                        dt = datetime.fromisoformat(sent_time.replace('Z', '+00:00'))
                        st.write(f"Sent: {dt.strftime('%Y-%m-%d %H:%M')}")
                    except:
                        st.write(f"Sent: {sent_time}")
                
                # Show urgency level if available
                urgency = message.get('UrgencyLevel')
                if urgency:
                    urgency_color = "🔴" if urgency >= 4 else "🟡" if urgency >= 2 else "🟢"
                    st.write(f"{urgency_color} Level {urgency}")
            
            st.divider()
else:
    st.info("No messages found. Send a message to get started!")

# Sidebar additional features
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Message preferences
    st.checkbox("Email notifications", value=True)
    st.checkbox("SMS notifications", value=False)
    st.checkbox("Desktop notifications", value=True)
    
    # Message filters
    st.markdown("### 🔍 Filters")
    show_read = st.checkbox("Show read messages", value=True)
    show_unread = st.checkbox("Show unread messages", value=True)
    
    # Refresh button
    if st.button("🔄 Refresh Messages"):
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*VitalFlow Messaging System - Secure healthcare communication*")
