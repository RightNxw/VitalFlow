"""
VitalFlow Medical App - Styling Module
Provides consistent CSS styling across all pages
"""

import streamlit as st
import os

def load_css():
    """
    Load the main CSS file for the medical app
    """
    css_file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'medical_app.css')
    
    try:
        with open(css_file_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        # Fallback CSS if file not found
        st.markdown("""
        <style>
        /* Fallback styling */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }
        </style>
        """, unsafe_allow_html=True)
        st.warning("CSS file not found. Using fallback styling.")

def apply_medical_theme():
    """
    Apply the medical theme configuration to Streamlit
    """
    # Set page config with medical theme
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🏥"
    )
    
    # Load custom CSS
    load_css()

def get_status_color(severity):
    """
    Get the appropriate status color based on severity level
    
    Args:
        severity (str): Severity level (critical, warning, stable, normal)
    
    Returns:
        str: CSS class name for the status
    """
    severity_map = {
        'critical': 'status-critical',
        'warning': 'status-warning', 
        'stable': 'status-stable',
        'normal': 'status-normal',
        'high': 'status-critical',
        'medium': 'status-warning',
        'low': 'status-stable'
    }
    
    return severity_map.get(severity.lower(), 'status-normal')

def create_metric_card(value, label, icon="📊", color="primary"):
    """
    Create a styled metric card
    
    Args:
        value: The metric value to display
        label (str): The label for the metric
        icon (str): Emoji icon for the metric
        color (str): Color theme (primary, success, warning, danger)
    
    Returns:
        str: HTML for the metric card
    """
    color_classes = {
        "primary": "var(--primary-blue)",
        "success": "var(--accent-green)", 
        "warning": "var(--accent-orange)",
        "danger": "var(--accent-red)"
    }
    
    selected_color = color_classes.get(color, color_classes["primary"])
    
    return f"""
    <div class="metric-card" style="border-top: 3px solid {selected_color};">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-value" style="color: {selected_color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def create_patient_card(patient_data, clickable=True):
    """
    Create a styled patient card
    
    Args:
        patient_data (dict): Patient information
        clickable (bool): Whether the card should be clickable
    
    Returns:
        str: HTML for the patient card
    """
    first_name = patient_data.get('FirstName', 'N/A')
    last_name = patient_data.get('LastName', 'N/A')
    initials = f"{first_name[0] if first_name else 'P'}{last_name[0] if last_name else 'T'}"
    
    # Get additional patient info
    dob = patient_data.get('DOB', 'N/A')
    blood_type = patient_data.get('BloodType', 'N/A')
    
    click_class = "patient-card" if clickable else "patient-card"
    
    return f"""
    <div class="{click_class}">
        <div class="patient-avatar">{initials}</div>
        <div class="patient-info">
            <div class="patient-field">
                <strong>{first_name} {last_name}</strong>
            </div>
            <div class="patient-field">DOB: {dob}</div>
            <div class="patient-field">Blood Type: {blood_type}</div>
        </div>
    </div>
    """

def create_alert_card(title, description, severity="info", timestamp=None):
    """
    Create a styled alert card
    
    Args:
        title (str): Alert title
        description (str): Alert description
        severity (str): Alert severity (critical, warning, info, success)
        timestamp (str): Optional timestamp
    
    Returns:
        str: HTML for the alert card
    """
    severity_class = f"alert-card {severity.lower()}"
    
    timestamp_html = ""
    if timestamp:
        timestamp_html = f'<div style="font-size: 0.8rem; color: var(--gray-500); margin-top: 0.5rem;">{timestamp}</div>'
    
    return f"""
    <div class="{severity_class}">
        <h4 style="margin: 0 0 0.5rem 0; color: var(--gray-800);">{title}</h4>
        <p style="margin: 0; color: var(--gray-600);">{description}</p>
        {timestamp_html}
    </div>
    """

def create_medical_divider():
    """
    Create a styled medical-themed divider
    
    Returns:
        str: HTML for the divider
    """
    return '<div class="medical-divider"></div>'

def add_medical_icon(icon="🏥"):
    """
    Add a medical icon with styling
    
    Args:
        icon (str): Emoji icon to display
    
    Returns:
        str: HTML for the medical icon
    """
    return f'<span class="medical-icon">{icon}</span>'

def apply_page_styling():
    """
    Apply comprehensive page styling including CSS and theme
    """
    apply_medical_theme()
    
    # Additional page-specific styling
    st.markdown("""
    <style>
    /* Ensure proper spacing and layout */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Improve form element spacing */
    .stTextInput, .stSelectbox, .stNumberInput {
        margin-bottom: 1rem;
    }
    
    /* Better table styling */
    .dataframe {
        margin: 1rem 0;
    }
    
    /* Improve button spacing */
    .stButton {
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
