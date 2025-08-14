# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator
 
# This file has function to add certain functionality to the left side bar of the app
 
import streamlit as st
 
 
#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")
 
 
def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")
 
 
#### ------------------------ Examples for Role of doctor ------------------------
def DoctorHomeNav():
    # Doctor portal navigation
    st.sidebar.page_link("pages/doctor_home.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/doctor_patients.py", label="Patients", icon="👥")
    st.sidebar.page_link("pages/doctor_alerts.py", label="Alerts", icon="⚠️")
    st.sidebar.page_link("pages/doctor_inbox.py", label="Inbox", icon="📥")
 
 
 
def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )
 
 
def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")
 
 
## ------------------------ Examples for Role of usaid_worker ------------------------

## these need to be updated to correct user personas of Nurse, Patient, Doctor!!! @Paulo @Ronak
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")
 
 
def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )
 
 
def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )
 
 
def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")
 
 
def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")
 
 
#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )

#### ------------------------ Nurse Role ------------------------
def NurseDashboardNav():
    st.sidebar.page_link("pages/xx_Nurse_Dashboard.py", label="Dashboard", icon="👩‍⚕️")


def NursePatientsNav():
    st.sidebar.page_link("pages/xx_Nurse_Patients.py", label="Patients", icon="👥")


def NurseTreatmentsNav():
    st.sidebar.page_link("pages/xx_Nurse_Treatments.py", label="Treatments", icon="💊")


def NurseAlertsNav():
    st.sidebar.page_link("pages/xx_Nurse_Alerts.py", label="Alerts", icon="⚠️")


def NurseInboxNav():
    st.sidebar.page_link("pages/xx_Nurse_Inbox.py", label="Inbox", icon="📥")


#### ------------------------ Patient Role ------------------------
def PatientHomeNav():
    st.sidebar.page_link("pages/50_Patient_Home.py", label="Home", icon="🏠")


def PatientPortalNav():
    st.sidebar.page_link("pages/50_Patient_Home.py", label="Portal", icon="❤️")


def PatientBillingNav():
    st.sidebar.page_link("pages/50_Patient_Home.py", label="Billing", icon="💰")


def PatientInboxNav():
    st.sidebar.page_link("pages/50_Patient_Home.py", label="Inbox", icon="📬")


def PatientSettingsNav():
    st.sidebar.page_link("pages/50_Patient_Home.py", label="Settings", icon="⚙️")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """
 
    ## add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)
 
    ## If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")
 
    if show_home:
        ## Show the Home page link (the landing page)
        HomeNav()
 
    ## Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        if st.session_state["role"] == "nurse":
            NurseDashboardNav()
            NursePatientsNav()
            NurseTreatmentsNav()
            NurseAlertsNav()
            NurseInboxNav()

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
 
        ## Show doctor portal navigation if the user is a doctor role.
        if st.session_state["role"] == "doctor":
            DoctorHomeNav()
 
        ## Show patient portal navigation if the user is a patient role.
        if st.session_state["role"] == "patient":
            PatientHomeNav()
            PatientPortalNav()
            PatientBillingNav()
            PatientInboxNav()
            PatientSettingsNav()
 
        ## If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()
            NgoDirectoryNav()
            AddNgoNav()
 
        ## If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
 
    ## Always show the About page at the bottom of the list of links
    AboutPageNav()
 
    if st.session_state["authenticated"]:
        ## Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")