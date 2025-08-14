## Patient Home Page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Patient Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

## Add logo and navigation
SideBarLinks()

## API configuration
API_BASE_URL = "http://web-api:4000"

## App state for navigation
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"

## API functions with better error handling and fallback data
def get_patient_info(patient_id):
    """Get patient information from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning(f"Patient with ID {patient_id} not found")
            return None
        else:
            st.warning(f"API returned status {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to patient API. Using demo data.")
        # Return consistent demo data for patient ID 1 (Alice Smith)
        return {
            "PatientID": 1,
            "FirstName": "Alice",
            "LastName": "Smith", 
            "DOB": "1980-05-15",
            "BloodType": "O+",
            "Weight": 145.5,
            "InsuranceID": 11,
            "VisitID": 1,
            "VitalID": 1,
            "ConditionID": 1,
            "DoctorID": 2,
            "NurseID": 1
        }
    except requests.exceptions.Timeout:
        st.warning("API request timed out. Using demo data.")
        return get_patient_info(1)  # Return demo data
    except Exception as e:
        st.error(f"Error retrieving patient information: {str(e)}")
        return None

def get_patient_visit(patient_id):
    """Get patient's current visit from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/visit", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            st.warning(f"Visit API returned status {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to visit API. Using demo data.")
        # Return consistent demo data for patient ID 1
        return {
            "VisitID": 1,
            "AdmitReason": "Annual physical examination",
            "AppointmentDate": "2024-01-15",
            "NextVisitDate": "2025-01-15"
        }
    except requests.exceptions.Timeout:
        st.warning("Visit API request timed out. Using demo data.")
        return get_patient_visit(1)  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving visit information: {str(e)}")
        return None

def get_patient_vitals(patient_id):
    """Get patient's current vitals from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/vitals", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            st.warning(f"Vitals API returned status {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to vitals API. Using demo data.")
        # Return consistent demo data for patient ID 1
        return {
            "VitalID": 1,
            "HeartRate": 72,
            "BloodPressure": "120/80",
            "RespiratoryRate": 16,
            "Temperature": 98.6
        }
    except requests.exceptions.Timeout:
        st.warning("Vitals API request timed out. Using demo data.")
        return get_patient_vitals(1)  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving vitals: {str(e)}")
        return None

def get_patient_medications(patient_id):
    """Get patient's medications from database"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/medications", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            st.warning(f"Medications API returned status {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to medications API. Using demo data.")
        # Return consistent demo data for patient ID 1
        return [
            {
                "MedicationID": 16,
                "PrescriptionName": "Furosemide",
                "DosageAmount": 40,
                "DosageUnit": "mg",
                "PickUpLocation": "CVS Pharmacy - Main St",
                "RefillsLeft": 4,
                "FrequencyAmount": 2,
                "FrequencyPeriod": "daily",
                "PrescribedDate": "2024-07-15",
                "EndDate": None
            }
        ]
    except requests.exceptions.Timeout:
        st.warning("Medications API request timed out. Using demo data.")
        return get_patient_medications(1)  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving medications: {str(e)}")
        return []

def get_patient_insurance(patient_id):
    """Get patient's insurance information"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}/insurance", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            st.warning(f"Insurance API returned status {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to insurance API. Using demo data.")
        # Return consistent demo data for patient ID 1
        return {
            "InsuranceID": 11,
            "InsuranceProvider": "Blue Cross Blue Shield",
            "PolicyNumber": "BCBS-2024-011",
            "Deductible": 650.00,
            "DueDate": "2024-02-29"
        }
    except requests.exceptions.Timeout:
        st.warning("Insurance API request timed out. Using demo data.")
        return get_patient_insurance(1)  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving insurance: {str(e)}")
        return None

def get_patient_messages(patient_id):
    """Get messages for specific patient"""
    try:
        response = requests.get(f"{API_BASE_URL}/message/?user_type=patient&user_id={patient_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            st.warning(f"Messages API returned status {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to messages API. Using demo data.")
        # Return consistent demo data for patient ID 1
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
    except requests.exceptions.Timeout:
        st.warning("Messages API request timed out. Using demo data.")
        return get_patient_messages(1)  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving messages: {str(e)}")
        return get_patient_messages(1)  # Return demo data

def get_doctors():
    """Get all doctors for recipient selection"""
    try:
        response = requests.get(f"{API_BASE_URL}/doctor/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"Doctors API returned status {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to doctors API. Using demo data.")
        return [
            {"DoctorID": 1, "FirstName": "Maya", "LastName": "Ellison", "Specialty": "Cardiology"},
            {"DoctorID": 2, "FirstName": "Michael", "LastName": "Chen", "Specialty": "Internal Medicine"},
            {"DoctorID": 3, "FirstName": "Emily", "LastName": "Rodriguez", "Specialty": "Pediatrics"}
        ]
    except requests.exceptions.Timeout:
        st.warning("Doctors API request timed out. Using demo data.")
        return get_doctors()  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving doctors: {str(e)}")
        return []

def get_nurses():
    """Get all nurses for recipient selection"""
    try:
        response = requests.get(f"{API_BASE_URL}/nurse/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"Nurses API returned status {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to nurses API. Using demo data.")
        return [
            {"NurseID": 1, "FirstName": "Amy", "LastName": "Thompson"},
            {"NurseID": 2, "FirstName": "John", "LastName": "Miller"},
            {"NurseID": 3, "FirstName": "Patricia", "LastName": "Jones"}
        ]
    except requests.exceptions.Timeout:
        st.warning("Nurses API request timed out. Using demo data.")
        return get_nurses()  # Return demo data
    except Exception as e:
        st.warning(f"Error retrieving nurses: {str(e)}")
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

def create_new_visit(patient_id, admit_reason, appointment_date):
    """Create a new visit in the database"""
    try:
        visit_data = {
            "AdmitReason": admit_reason,
            "AppointmentDate": appointment_date.isoformat()
        }
        response = requests.post(f"{API_BASE_URL}/visit/", json=visit_data)
        if response.status_code == 201:
            visit_id = response.json().get("visit_id")
            if visit_id:
                # Link the visit to the patient
                update_data = {"VisitID": visit_id}
                update_response = requests.put(f"{API_BASE_URL}/patient/{patient_id}", json=update_data)
                if update_response.status_code == 200:
                    return True
        return False
    except:
        return False

## Main page logic
def main():
    if st.session_state.current_view == "home":
        show_patient_home()
    elif st.session_state.current_view == "billing":
        show_patient_billing()
    elif st.session_state.current_view == "inbox":
        show_patient_inbox()

def show_patient_home():
    """Show the main patient home page"""
    st.markdown("<h1 style='text-align: center;'>Patient Portal</h1>", unsafe_allow_html=True)
    
    # Get current patient ID from session state (assuming patient is logged in)
    patient_id = st.session_state.get('current_patient_id', 1)  # Default to patient ID 1 for demo
    
    # Get patient data from database
    patient_info = get_patient_info(patient_id)
    if not patient_info:
        st.error("Could not load patient information")
        st.stop()
    
    # Extract patient name from database
    patient_name = f"{patient_info.get('FirstName', 'Unknown')} {patient_info.get('LastName', 'Unknown')}"
    patient_dob = patient_info.get('DOB', 'Unknown')
    
    # Patient Profile section
    st.markdown("---")
    st.markdown(f"**{patient_name}**")
    st.markdown(f"**Patient DOB:** {patient_dob}")

    # Bottom section: Visits
    st.markdown("---")
    st.markdown("### **VISITS**")
    
    # Get current visit from database
    current_visit = get_patient_visit(patient_id)
    
    if current_visit:
        # Display current visit info from database
        st.info("**Current Visit Information:**")
        st.markdown(f"**Patient Admit Date:** {current_visit.get('AppointmentDate', 'N/A')}")
        st.markdown(f"**Admit Reason:** {current_visit.get('AdmitReason', 'N/A')}")
        if current_visit.get('NextVisitDate'):
            st.markdown(f"**Next Visit:** {current_visit.get('NextVisitDate', 'N/A')}")
    else:
        st.info("No current visit found")

    # Form to create new visit
    st.markdown("**Schedule New Visit:**")
    with st.form("new_visit_form"):
        admit_reason = st.text_input("Admit Reason", placeholder="Enter reason for visit...")
        appointment_date = st.date_input("Appointment Date", value=datetime.now().date())
        
        if st.form_submit_button("Schedule Visit"):
            if admit_reason and appointment_date:
                if create_new_visit(patient_id, admit_reason, appointment_date):
                    st.success("Visit scheduled successfully!")
                    st.rerun()
                else:
                    st.error("Failed to schedule visit")
            else:
                st.error("Please fill in all fields")

def show_patient_billing():
    """Show patient billing and insurance information"""
    # Get current patient ID from session state
    patient_id = st.session_state.get('current_patient_id', 1)
    patient_info = get_patient_info(patient_id)
    
    if not patient_info:
        st.error("Could not load patient information")
        return
    
    patient_name = f"{patient_info.get('FirstName', 'Unknown')} {patient_info.get('LastName', 'Unknown')}"
    
    # Header with back button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 💰 Billing & Insurance: {patient_name}")
    with col2:
        if st.button("← Back to Home"):
            st.session_state.current_view = "home"
            st.rerun()
    
    # Get insurance information
    insurance_info = get_patient_insurance(patient_id)
    
    # Get visit information for billing context
    visit_info = get_patient_visit(patient_id)
    
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
    
    # Billing Actions
    st.markdown("### 💳 Billing Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Generate Bill", use_container_width=True):
            st.info("Billing system integration would be implemented here")
    
    with col2:
        if st.button("📊 View Payment History", use_container_width=True):
            st.info("Payment history would be displayed here")

def show_patient_inbox():
    """Show patient inbox and messaging system"""
    # Get current patient ID from session state
    patient_id = st.session_state.get('current_patient_id', 1)
    patient_info = get_patient_info(patient_id)
    
    if not patient_info:
        st.error("Could not load patient information")
        return
    
    patient_name = f"{patient_info.get('FirstName', 'Unknown')} {patient_info.get('LastName', 'Unknown')}"
    
    # Header with back button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 📬 Messages & Communications: {patient_name}")
    with col2:
        if st.button("← Back to Home"):
            st.session_state.current_view = "home"
            st.rerun()
    
    # Get messages for this patient
    messages = get_patient_messages(patient_id)
    
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
                create_message(subject, content, st.session_state.recipient_type, recipient_id, priority, patient_id, "Patient")
                
            else:
                st.warning("Please fill in all required fields.")

## Run the main app
if __name__ == "__main__":
    main()
