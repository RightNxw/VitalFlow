

## doctor inbox page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
 
# Add logo and navigation
SideBarLinks()
 
# Page config
st.set_page_config(
    page_title="Doctor Portal - Inbox",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
st.write("# Messages & Communications")
st.write("View and manage your messages.")
 
# API configuration
API_BASE_URL = "http://web-api:4000"
 
# API functions
def get_messages(doctor_id):
    """Get messages for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/messages?user_type=doctor&user_id={doctor_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [{"MessageID": 1, "Subject": "Patient Update", "Content": "Patient condition improved", "Priority": "Normal"}]
 
# Get messages for current doctor
doctor_id = st.session_state.get('current_doctor_id', 1)
messages = get_messages(doctor_id)
 
if not messages:
    st.info("No messages in your inbox.")
    st.stop()
 
# Display messages
for message in messages:
    with st.expander(f"📧 {message.get('Subject', 'No Subject')} - {message.get('Timestamp', 'N/A')}"):
        st.markdown(f"**From:** {message.get('SenderType', 'Unknown')} {message.get('SenderID', 'N/A')}")
        st.markdown(f"**Content:** {message.get('Content', 'No content')}")
        st.markdown(f"**Read:** {'Yes' if message.get('ReadStatus') else 'No'}")
        st.markdown(f"**Priority:** {message.get('Priority', 'Normal')}")