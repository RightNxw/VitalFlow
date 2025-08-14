##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# Import styling module
from modules.styles import apply_page_styling

# Apply medical theme and styling
apply_page_styling()

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")

# Medical-themed header
st.markdown("""
<div style="text-align: center; margin: 3rem 0;">
    <h1 style="margin-bottom: 1rem; font-size: 3.5rem;">🏥 VitalFlow</h1>
    <p style="font-size: 1.3rem; color: var(--gray-600); margin-bottom: 2rem;">
        Advanced Medical Information Management System
    </p>
    <div class="medical-divider" style="margin: 0 auto; width: 200px;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h2 style="color: var(--primary-blue); margin-bottom: 1rem;">👋 Welcome to VitalFlow!</h2>
    <p style="font-size: 1.1rem; color: var(--gray-600); margin-bottom: 2rem;">
        Please select your role to access the appropriate portal
    </p>
</div>
""", unsafe_allow_html=True)

# Create a container for the role selection buttons
st.markdown("""
<div style="max-width: 800px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 3rem;">
        <h3 style="color: var(--gray-700); margin-bottom: 1rem;">Select Your Role</h3>
        <p style="color: var(--gray-600);">Choose the appropriate portal for your role</p>
    </div>
</div>
""", unsafe_allow_html=True)

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

# Create columns for better button layout
col1, col2 = st.columns(2)

with col1:
    if st.button("👩‍⚕️ Act as Nic, a Nurse", 
                type='primary', 
                use_container_width=True,
                help="Access the nurse portal for patient care and treatment management"):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'nurse'
        # we add the first name of the user (so it can be displayed on 
        # subsequent pages). 
        st.session_state['first_name'] = 'Nic'
        # finally, we ask streamlit to switch to another page, in this case, the 
        # landing page for this particular user type
        logger.info("Logging in as Nurse Persona")
        st.switch_page('pages/xx_Nurse_Dashboard.py')

    if st.button("👨‍⚕️ Act as Maya, a Doctor", 
                type='primary', 
                use_container_width=True,
                help="Access the doctor portal for patient diagnosis and treatment"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'doctor'
        st.session_state['first_name'] = 'Maya'
        logger.info("Logging in as Doctor Persona")
        st.switch_page('pages/doctor_home.py')

with col2:
    if st.button("👤 Act as Joe, a Patient", 
                type='primary', 
                use_container_width=True,
                help="Access the patient portal for personal health information"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'patient'
        st.session_state['first_name'] = 'Joe'
        st.session_state['current_patient_id'] = 1  # Default to patient ID 1
        logger.info("Logging in as Patient Persona")
        st.switch_page('pages/50_Patient_Home.py')

    if st.button('👥 Act as Nina Pesci, a Proxy',  ## Updated to Proxy
                type = 'primary', 
                use_container_width=True,
                help="Access the proxy portal for managing dependent patients"):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'proxy'
        st.session_state['first_name'] = 'Nina'
        st.switch_page('pages/proxy_home.py')



