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


#### ------------------------ Examples for Role of proxy ------------------------
def ProxyHomeNav():
    # Proxy portal navigation
    
    st.sidebar.page_link("pages/proxy_home.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/proxy_portal.py", label="Portal", icon="👥")
    st.sidebar.page_link("pages/proxy_billing.py", label="Billing", icon="💰")
    st.sidebar.page_link("pages/proxy_messages.py", label="Inbox", icon="📥")


 
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
 
        ## Show doctor portal navigation if the user is a doctor role.
        if st.session_state["role"] == "doctor":
            DoctorHomeNav()

        ## Show proxy portal navigation if the user is a proxy role.
        if st.session_state["role"] == "proxy":
            ProxyHomeNav()
 
    ## Always show the About page at the bottom of the list of links
    AboutPageNav()
 
    if st.session_state["authenticated"]:
        ## Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")