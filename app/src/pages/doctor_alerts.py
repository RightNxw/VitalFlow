
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
st.set_page_config(
    page_title="Doctor Portal - Alerts",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
st.write("# Patient Alerts")
st.write("View and manage patient alerts.")
 
## API configuration
API_BASE_URL = "http://web-api:4000"
 
## API functions
def get_alerts(doctor_id):
    """Get alerts for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/alerts?user_type=doctor&user_id={doctor_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [{"AlertID": 1, "Title": "High Blood Pressure", "Description": "Patient BP elevated", "Severity": "High"}]
 
## Get alerts for current doctor
doctor_id = st.session_state.get('current_doctor_id', 1)
alerts = get_alerts(doctor_id)
 
if not alerts:
    st.info("No active alerts at this time.")
    st.stop()
 
##  Display alerts
for alert in alerts:
    with st.expander(f"⚠️ {alert.get('Title', 'Alert')} - {alert.get('Severity', 'Medium')}"):
        st.markdown(f"**Description:** {alert.get('Description', 'No description')}")
        st.markdown(f"**Patient ID:** {alert.get('PatientID', 'N/A')}")
        st.markdown(f"**Timestamp:** {alert.get('Timestamp', 'N/A')}")
        st.markdown(f"**Acknowledged:** {'Yes' if alert.get('Acknowledged') else 'No'}")
 
        if not alert.get('Acknowledged'):
            if st.button(f"Acknowledge Alert {alert.get('AlertID')}", key=f"ack_{alert.get('AlertID')}"):
                st.success("Alert acknowledged!")
                st.rerun()