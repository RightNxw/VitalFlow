
## doctor alerts page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
 
## Add logo and navigation
SideBarLinks()
 
## Page config

 
st.write("# Patient Alerts")
st.write("View and manage patient alerts.")
 
## API configuration
API_BASE_URL = "http://web-api:4000"
 
## API functions
def get_alerts(doctor_id):
    """Get alerts for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/alert/?user_type=doctor&user_id={doctor_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [
            {
                "AlertID": 1, 
                "Message": "Patient blood pressure critically high: 180/110", 
                "PostedBy": 2, 
                "PostedByRole": "Nurse", 
                "Protocol": "Immediate intervention required. Administer antihypertensive medication.", 
                "SentTime": "Thu, 14 Aug 2025 01:49:01 GMT", 
                "UrgencyLevel": 5
            }
        ]
 
## Get alerts for current doctor
doctor_id = st.session_state.get('current_doctor_id', 1)
alerts = get_alerts(doctor_id)
 
if not alerts:
    st.info("No active alerts at this time.")
    st.stop()
 
##  Display alerts
for alert in alerts:
    # Get urgency level with color coding
    urgency = alert.get('UrgencyLevel', 1)
    urgency_text = f"Level {urgency}"
    urgency_color = "🔴" if urgency >= 4 else "🟡" if urgency >= 2 else "🟢"
    
    with st.expander(f"{urgency_color} Alert #{alert.get('AlertID', 'N/A')} - {urgency_text}", expanded=True):
        st.markdown(f"**Message:** {alert.get('Message', 'No message')}")
        st.markdown(f"**Protocol:** {alert.get('Protocol', 'No protocol')}")
        st.markdown(f"**Posted By:** {alert.get('PostedByRole', 'Unknown')} (ID: {alert.get('PostedBy', 'N/A')})")
        st.markdown(f"**Sent Time:** {alert.get('SentTime', 'N/A')}")
        
        # Add action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Acknowledge", key=f"ack_{alert.get('AlertID')}"):
                st.success("Alert acknowledged!")
        with col2:
            pass  # Removed View Details button
 