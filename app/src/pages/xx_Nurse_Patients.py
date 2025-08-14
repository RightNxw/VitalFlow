import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from modules.nav import SideBarLinks
from modules.styles import apply_page_styling, create_metric_card, create_patient_card, create_medical_divider

<<<<<<< Updated upstream
=======

from modules.styles import apply_page_styling, create_metric_card, create_patient_card, create_medical_divider

>>>>>>> Stashed changes
## Apply medical theme and styling
apply_page_styling()

SideBarLinks()

API_BASE = os.getenv("API_BASE")
DEFAULT_NURSE_ID = int(os.getenv("DEFAULT_NURSE_ID", "0") or 0)
try:
    from modules.config import API_BASE as CFG_API_BASE, DEFAULT_NURSE_ID as CFG_NURSE_ID
    API_BASE = API_BASE or CFG_API_BASE
    DEFAULT_NURSE_ID = DEFAULT_NURSE_ID or int(CFG_NURSE_ID)
except Exception:
    pass
if not API_BASE:
    if os.path.exists('/.dockerenv'):
        API_BASE = "http://web-api:4000"
    else:
        API_BASE = "http://localhost:4000"
if DEFAULT_NURSE_ID == 0:
    DEFAULT_NURSE_ID = 2


def list_patients():
    try:
        r = requests.get(f"{API_BASE}/patient/", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /patient/ → {r.status_code}")
            return []
        return r.json() or []
    except requests.exceptions.RequestException as ex:
        st.error(f"Patients service unreachable at {API_BASE}. Details: {ex}")
        return []


def get_patient(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/{pid}", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /patient/{pid} → {r.status_code}")
            return None
        return r.json()
    except requests.exceptions.RequestException as ex:
        st.error(f"Patient detail unreachable. Details: {ex}")
        return None


def get_patient_vitals(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/{pid}/vitals", timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


def get_patient_condition(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/{pid}/condition", timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


<<<<<<< Updated upstream
def get_patient_medications(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/{pid}/medications", timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


=======
>>>>>>> Stashed changes
# Medical-themed header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">👥 Patient Management</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        View and manage your assigned patients
    </p>
</div>
""", unsafe_allow_html=True)

# Controls section
st.markdown("""
<div style="margin: 2rem 0;">
    <h3 style="color: var(--primary-blue); margin-bottom: 1rem;">🔍 Search & Filters</h3>
</div>
""", unsafe_allow_html=True)

ctrl_l, ctrl_r = st.columns([3, 1])
with ctrl_l:
    q = st.text_input("Search name, blood type…", placeholder="Enter search terms...")
    only_mine = st.checkbox("Only my patients", value=True)
    refresh = st.button("🔄 Refresh", type="primary", use_container_width=True)
with ctrl_r:
    pass  # Removed NurseID input since we know which nurse is logged in

patients = list_patients()
df = pd.DataFrame(patients)
if not df.empty:
    # Filters
    if only_mine and "NurseID" in df.columns:
        df = df[df["NurseID"].astype(str) == str(int(DEFAULT_NURSE_ID))]
    if q:
        ql = q.lower()
        cols = [c for c in ["FirstName", "LastName", "BloodType"] if c in df.columns]
        if cols:
            df = df[df[cols].astype(str).apply(lambda r: any(ql in str(x).lower() for x in r), axis=1)]
    sort_cols = [c for c in ["LastName", "FirstName", "PatientID"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(by=sort_cols)

# Add medical divider
st.markdown(create_medical_divider(), unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown("""
    <div style="margin: 1rem 0;">
        <h3 style="color: var(--primary-blue); margin-bottom: 1rem;">📋 Patient List</h3>
        <p style="color: var(--gray-600); margin: 0;">Select a patient to view detailed information</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display patients using beautiful cards
    if not df.empty:
        for _, patient in df.iterrows():
            patient_dict = patient.to_dict()
            st.markdown(create_patient_card(patient_dict), unsafe_allow_html=True)
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📋 View Details", key=f"view_{patient_dict.get('PatientID')}", use_container_width=True, type="primary"):
                    st.session_state["selected_patient_id"] = int(patient_dict.get('PatientID', 0))
                    st.rerun()
            with col2:
                if st.button(f"💊 View Meds", key=f"meds_{patient_dict.get('PatientID')}", use_container_width=True, type="primary"):
                    st.session_state["selected_patient_id"] = int(patient_dict.get('PatientID', 0))
<<<<<<< Updated upstream
                    st.session_state["show_medications"] = True
=======
>>>>>>> Stashed changes
                    st.rerun()
            
            # Add medical divider between patients
            st.markdown(create_medical_divider(), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="medical-card" style="text-align: center; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);">
            <h4 style="color: var(--gray-700); margin-bottom: 0.5rem;">📋 No Patients Found</h4>
            <p style="color: var(--gray-600); margin: 0;">No patients match your current filters.</p>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div style="margin: 1rem 0;">
        <h3 style="color: var(--secondary-teal); margin-bottom: 1rem;">🔍 Quick Details</h3>
        <p style="color: var(--gray-600); margin: 0;">Patient information and vitals</p>
    </div>
    """, unsafe_allow_html=True)
    
    pid = st.session_state.get("selected_patient_id", 0)
    if pid:
        p = get_patient(int(pid))
        v = get_patient_vitals(int(pid))
        c = get_patient_condition(int(pid))
        
        if p:
            st.markdown("""
            <div class="medical-card" style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);">
                <h4 style="color: var(--primary-blue); margin-bottom: 1rem;">👤 Patient Info</h4>
                <p><strong>PatientID:</strong> {patient_id}</p>
                <p><strong>Name:</strong> {first_name} {last_name}</p>
                <p><strong>DOB:</strong> {dob}</p>
                <p><strong>BloodType:</strong> {blood_type}</p>
            </div>
            """.format(
                patient_id=p.get('PatientID', '-'),
                first_name=p.get('FirstName', ''),
                last_name=p.get('LastName', ''),
                dob=p.get('DOB', '-'),
                blood_type=p.get('BloodType', '-')
            ), unsafe_allow_html=True)
        
        if v:
<<<<<<< Updated upstream
            # Handle vitals data - it might be a list or dict
            if isinstance(v, list) and len(v) > 0:
                v = v[0]  # Take the first vitals record
            elif not isinstance(v, dict):
                v = {}
                
=======
>>>>>>> Stashed changes
            st.markdown("""
            <div class="medical-card" style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); margin-top: 1rem;">
                <h4 style="color: var(--accent-green); margin-bottom: 1rem;">💓 Vitals</h4>
                <p><strong>HR:</strong> {hr}</p>
                <p><strong>BP:</strong> {bp}</p>
                <p><strong>RR:</strong> {rr}</p>
                <p><strong>Temp:</strong> {temp}</p>
            </div>
            """.format(
                hr=v.get('HeartRate', '-'),
                bp=v.get('BloodPressure', '-'),
                rr=v.get('RespiratoryRate', '-'),
                temp=v.get('Temperature', '-')
            ), unsafe_allow_html=True)
        
        if c:
<<<<<<< Updated upstream
            # Handle condition data - it might be a list or dict
            if isinstance(c, list) and len(c) > 0:
                c = c[0]  # Take the first condition record
            elif not isinstance(c, dict):
                c = {}
                
=======
>>>>>>> Stashed changes
            st.markdown("""
            <div class="medical-card" style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); margin-top: 1rem;">
                <h4 style="color: var(--accent-orange); margin-bottom: 1rem;">🏥 Condition</h4>
                <p><strong>Description:</strong> {desc}</p>
                <p><strong>Treatment:</strong> {treatment}</p>
            </div>
            """.format(
                desc=c.get("Description", "-"),
                treatment=c.get("Treatment", "-")
            ), unsafe_allow_html=True)
<<<<<<< Updated upstream
        
        # Add medications section
        m = get_patient_medications(int(pid))
        if m:
            # Handle medications data - it might be a list or dict
            if isinstance(m, list) and len(m) > 0:
                m = m[0]  # Take the first medication record
            elif not isinstance(m, dict):
                m = {}
                
            st.markdown("""
            <div class="medical-card" style="background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%); margin-top: 1rem;">
                <h4 style="color: var(--accent-pink); margin-bottom: 1rem;">💊 Medications</h4>
                <p><strong>Prescription:</strong> {prescription}</p>
                <p><strong>Dosage:</strong> {dosage}</p>
                <p><strong>Frequency:</strong> {frequency}</p>
                <p><strong>Refills:</strong> {refills}</p>
            </div>
            """.format(
                prescription=m.get('PrescriptionName', '-'),
                dosage=f"{m.get('DosageAmount', '')} {m.get('DosageUnit', '')}",
                frequency=f"{m.get('FrequencyAmount', '')} {m.get('FrequencyPeriod', '')}",
                refills=m.get('RefillsLeft', '-')
            ), unsafe_allow_html=True)
=======
>>>>>>> Stashed changes
    else:
        st.markdown("""
        <div class="medical-card" style="text-align: center; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);">
            <h4 style="color: var(--gray-700); margin-bottom: 0.5rem;">👆 Select a Patient</h4>
            <p style="color: var(--gray-600); margin: 0;">Choose a patient from the list to view details</p>
        </div>
        """, unsafe_allow_html=True)
<<<<<<< Updated upstream

# Add medications view section
if st.session_state.get("show_medications", False) and st.session_state.get("selected_patient_id", 0):
    st.markdown(create_medical_divider(), unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: var(--primary-blue); margin-bottom: 1rem;">💊 Patient Medications</h2>
        <p style="color: var(--gray-600); margin: 0;">Detailed medication information for selected patient</p>
    </div>
    """, unsafe_allow_html=True)
    
    patient_id = st.session_state.get("selected_patient_id", 0)
    medications = get_patient_medications(patient_id)
    
    if medications:
        if isinstance(medications, list):
            for i, med in enumerate(medications):
                st.markdown(f"""
                <div class="medical-card" style="margin-bottom: 1rem;">
                    <h4 style="color: var(--accent-pink); margin-bottom: 1rem;">💊 Medication {i+1}</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <p><strong>Prescription:</strong> {med.get('PrescriptionName', '-')}</p>
                            <p><strong>Dosage:</strong> {med.get('DosageAmount', '')} {med.get('DosageUnit', '')}</p>
                            <p><strong>Frequency:</strong> {med.get('FrequencyAmount', '')} {med.get('FrequencyPeriod', '')}</p>
                        </div>
                        <div>
                            <p><strong>Refills Left:</strong> {med.get('RefillsLeft', '-')}</p>
                            <p><strong>Pickup Location:</strong> {med.get('PickUpLocation', '-')}</p>
                            <p><strong>Prescribed Date:</strong> {med.get('PrescribedDate', '-')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Single medication
            med = medications
            st.markdown(f"""
            <div class="medical-card">
                <h4 style="color: var(--accent-pink); margin-bottom: 1rem;">💊 Medication Details</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <p><strong>Prescription:</strong> {med.get('PrescriptionName', '-')}</p>
                        <p><strong>Dosage:</strong> {med.get('DosageAmount', '')} {med.get('DosageUnit', '')}</p>
                        <p><strong>Frequency:</strong> {med.get('FrequencyAmount', '')} {med.get('FrequencyPeriod', '')}</p>
                    </div>
                    <div>
                        <p><strong>Refills Left:</strong> {med.get('RefillsLeft', '-')}</p>
                        <p><strong>Pickup Location:</strong> {med.get('PickUpLocation', '-')}</p>
                        <p><strong>Prescribed Date:</strong> {med.get('PrescribedDate', '-')}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No medications found for this patient.")
    
    # Add a button to go back to patient list
    if st.button("← Back to Patient List", type="primary", use_container_width=True):
        st.session_state["show_medications"] = False
        st.rerun()
=======
>>>>>>> Stashed changes


