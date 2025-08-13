## Proxy Messages - Inbox & Alerts

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

## Add logo and navigation
SideBarLinks()

## Page config
st.set_page_config(
    page_title="Proxy Messages - Inbox & Alerts",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("# 📥 Inbox & Alerts")
st.write("View messages and alerts for your dependent patients.")

# API configuration
API_BASE_URL = "http://web-api:4000"

## API functions
def get_proxies():
    """Get all proxies from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/proxies")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to proxies API, using dummy data.")
        return [{"ProxyID": 1, "FirstName": "Nina", "LastName": "Pesci", "Relationship": "Child"}]

def get_alerts(proxy_id):
    """Get alerts for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/alerts?user_type=proxy&user_id={proxy_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [
            {"AlertID": 1, "Title": "Medication Refill", "Description": "Patient needs medication refill", "Severity": "Medium", "PatientName": "Joe Pesci", "Date": "2024-01-20"},
            {"AlertID": 2, "Title": "Appointment Reminder", "Description": "Upcoming appointment in 2 days", "Severity": "Low", "PatientName": "Maria Pesci", "Date": "2024-01-22"},
            {"AlertID": 3, "Title": "Test Results Available", "Description": "Lab results are ready for review", "Severity": "Low", "PatientName": "Joe Pesci", "Date": "2024-01-19"}
        ]

def get_messages(proxy_id):
    """Get messages for specific proxy"""
    try:
        response = requests.get(f"{API_BASE_URL}/messages?user_type=proxy&user_id={proxy_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to messages API, using dummy data.")
        return [
            {"MessageID": 1, "Subject": "Appointment Confirmation", "Content": "Your appointment has been confirmed for tomorrow at 2:00 PM", "Priority": "Normal", "From": "Dr. Smith", "Date": "2024-01-20", "Read": False},
            {"MessageID": 2, "Subject": "Insurance Update", "Content": "Your insurance information has been updated in our system", "Priority": "Normal", "From": "Billing Department", "Date": "2024-01-19", "Read": True},
            {"MessageID": 3, "Subject": "Care Plan Review", "Content": "It's time to review and update your care plan", "Priority": "High", "From": "Care Team", "Date": "2024-01-18", "Read": False}
        ]

## Get proxy information
proxies = get_proxies()
if proxies:
    current_proxy = proxies[0]
    proxy_id = current_proxy.get('ProxyID', 1)
else:
    proxy_id = 1

## Welcome message
if proxies:
    proxy_name = f"{proxies[0].get('FirstName', 'Nina')} {proxies[0].get('LastName', 'Pesci')}"
    st.markdown(f"### Welcome, {proxy_name}")
else:
    st.markdown("### Welcome, Nina Pesci")

st.markdown("---")

## Inbox Overview
st.markdown("## 📊 Inbox Overview")

alerts = get_alerts(proxy_id)
messages = get_messages(proxy_id)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_alerts = len(alerts)
    st.metric("Active Alerts", total_alerts)

with col2:
    total_messages = len(messages)
    st.metric("Total Messages", total_messages)

with col3:
    unread_messages = len([m for m in messages if not m.get('Read', False)])
    st.metric("Unread Messages", unread_messages)

with col4:
    high_priority = len([m for m in messages if m.get('Priority') == 'High'])
    st.metric("High Priority", high_priority)

st.markdown("---")

## Messages Section
st.markdown("## 📧 Messages")

if messages:
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Normal", "Low"])
    
    with col2:
        read_filter = st.selectbox("Filter by Status", ["All", "Unread", "Read"])
    
    with col3:
        search_query = st.text_input("Search Messages", placeholder="Search by subject or content...")
    
    # Filter messages
    filtered_messages = messages
    
    if priority_filter != "All":
        filtered_messages = [m for m in filtered_messages if m.get('Priority') == priority_filter]
    
    if read_filter == "Unread":
        filtered_messages = [m for m in filtered_messages if not m.get('Read', False)]
    elif read_filter == "Read":
        filtered_messages = [m for m in filtered_messages if m.get('Read', False)]
    
    if search_query:
        filtered_messages = [m for m in filtered_messages if 
                           search_query.lower() in m.get('Subject', '').lower() or 
                           search_query.lower() in m.get('Content', '').lower()]
    
    # Display filtered messages
    if filtered_messages:
        for message in filtered_messages:
            priority_color = "🔴" if message.get('Priority') == 'High' else "🟡" if message.get('Priority') == 'Normal' else "🟢"
            read_status = "📖" if message.get('Read') else "📬"
            
            with st.expander(f"{priority_color} {read_status} {message.get('Subject', 'No Subject')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **From:** {message.get('From', 'N/A')}
                    **Date:** {message.get('Date', 'N/A')}
                    **Priority:** {message.get('Priority', 'Normal')}
                    **Content:** {message.get('Content', 'No content')}
                    """)
                
                with col2:
                    if not message.get('Read', False):
                        if st.button("📖 Mark as Read", key=f"read_{message.get('MessageID')}", use_container_width=True):
                            st.info("Message marked as read")
                    
                    if st.button("📧 Reply", key=f"reply_{message.get('MessageID')}", use_container_width=True):
                        st.info("Reply functionality would open here")
                    
                    if st.button("🗑️ Delete", key=f"delete_{message.get('MessageID')}", use_container_width=True):
                        st.info("Message deleted")
                
                st.divider()
    else:
        st.info("No messages match your current filters.")
else:
    st.info("No messages in your inbox.")

st.markdown("---")

## Alerts Section
st.markdown("## ⚠️ Alerts")

if alerts:
    # Filter alerts by severity
    severity_filter = st.selectbox("Filter by Severity", ["All", "High", "Medium", "Low"])
    
    filtered_alerts = alerts
    if severity_filter != "All":
        filtered_alerts = [a for a in alerts if a.get('Severity') == severity_filter]
    
    if filtered_alerts:
        for alert in filtered_alerts:
            severity_color = "🔴" if alert.get('Severity') == 'High' else "🟡" if alert.get('Severity') == 'Medium' else "🟢"
            
            with st.expander(f"{severity_color} {alert.get('Title', 'Alert')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **Patient:** {alert.get('PatientName', 'N/A')}
                    **Date:** {alert.get('Date', 'N/A')}
                    **Severity:** {alert.get('Severity', 'Medium')}
                    **Description:** {alert.get('Description', 'No description')}
                    """)
                
                with col2:
                    if st.button("✅ Acknowledge", key=f"ack_{alert.get('AlertID')}", use_container_width=True):
                        st.info("Alert acknowledged")
                    
                    if st.button("📞 Contact Care Team", key=f"contact_{alert.get('AlertID')}", use_container_width=True):
                        st.info("Contact care team for this alert")
                
                st.divider()
    else:
        st.info("No alerts match your current severity filter.")
else:
    st.info("No active alerts.")

## Compose New Message
st.markdown("---")
st.markdown("## ✍️ Compose New Message")

with st.expander("📝 Write a new message", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.selectbox("To", ["Care Team", "Billing Department", "Dr. Smith", "Nurse Johnson"])
        subject = st.text_input("Subject", placeholder="Enter message subject...")
    
    with col2:
        priority = st.selectbox("Priority", ["Low", "Normal", "High"])
        patient = st.selectbox("Related Patient", ["Joe Pesci", "Maria Pesci", "General"])
    
    message_content = st.text_area("Message", placeholder="Type your message here...", height=150)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📤 Send Message", type="primary", use_container_width=True):
            if subject and message_content:
                st.success("Message sent successfully!")
            else:
                st.error("Please fill in all required fields.")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True):
            st.info("Draft saved")
