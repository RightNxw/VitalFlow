import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from modules.nav import SideBarLinks
from modules.styles import apply_page_styling, create_metric_card, create_patient_card, create_medical_divider

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


def get_patient_medications(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/{pid}/medications", timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


def administer_medication(patient_id: int, medication_id: int):
    """Administer medication to patient"""
    try:
        data = {
            "PatientID": patient_id,
            "MedicationID": medication_id
        }
        r = requests.post(f"{API_BASE}/medication/administer", json=data, timeout=10)
        if r.status_code == 200:
            return True, r.json().get("message", "Medication administered successfully")
        else:
            error_msg = r.json().get("error", f"Error {r.status_code}") if r.status_code != 500 else f"Server error {r.status_code}"
            return False, error_msg
    except requests.exceptions.RequestException as ex:
        return False, f"Service unreachable: {ex}"


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
df_pat = pd.DataFrame(patients)
if only_mine and not df_pat.empty and "NurseID" in df_pat.columns:
    df_pat = df_pat[df_pat["NurseID"].astype(str) == str(int(DEFAULT_NURSE_ID))]

# Patient selector
options = []
if not df_pat.empty:
    for _, row in df_pat.iterrows():
        label = f"{row.get('PatientID')} – {row.get('FirstName','')} {row.get('LastName','')}"
        options.append((int(row.get("PatientID")), label))

selected_label = None
if options:
    selected_label = st.selectbox("Select a patient", [label for _, label in options])
    selected_pid = next(pid for pid, label in options if label == selected_label)
else:
    selected_pid = 0
    st.info("No patients available with current filters.")

if selected_pid:
    p = get_patient(int(selected_pid))
    meds = get_patient_medications(int(selected_pid))

    # Header
    st.markdown("### 👤 Patient Summary")
    if p:
        st.markdown(f"""
        <div class="medical-card">
            <strong>Patient ID:</strong> {p.get('PatientID','-')}<br>
            <strong>Name:</strong> {p.get('FirstName','')} {p.get('LastName','')}<br>
            <strong>DOB:</strong> {p.get('DOB','-')}  •  <strong>Blood Type:</strong> {p.get('BloodType','-')}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(create_medical_divider(), unsafe_allow_html=True)
    st.markdown("### 💊 Current Prescriptions")
    df_m = pd.DataFrame(meds)
    if not df_m.empty:
        # Friendly column order if present
        order = [
            "PrescriptionName", "DosageAmount", "DosageUnit", "FrequencyAmount", "FrequencyPeriod",
            "PickUpLocation", "RefillsLeft", "PrescribedDate", "EndDate", "MedicationID"
        ]
        cols = [c for c in order if c in df_m.columns]
        # Ensure date-like columns render nicely
        for c in ["PrescribedDate", "EndDate"]:
            if c in df_m.columns:
                df_m[c] = pd.to_datetime(df_m[c], errors="coerce").dt.date
        
        st.dataframe(df_m[cols] if cols else df_m, use_container_width=True, hide_index=True)
    else:
        st.info("No medications linked to this patient.")

    st.markdown(create_medical_divider(), unsafe_allow_html=True)
    st.markdown("### 💉 Medication Administration")
    
    if not df_m.empty:
        # Create medication selection for administration
        med_options = []
        for _, med in df_m.iterrows():
            refills = med.get('RefillsLeft', 0) or 0
            if refills > 0:  # Only show medications with refills available
                label = f"{med.get('PrescriptionName', 'Unknown')} - {med.get('DosageAmount', '')} {med.get('DosageUnit', '')} ({refills} refills left)"
                med_options.append((med.get('MedicationID'), label))
        
        if med_options:
            selected_med_label = st.selectbox(
                "Select medication to administer", 
                [label for _, label in med_options],
                help="Only medications with available refills are shown"
            )
            
            if selected_med_label:
                selected_med_id = next(med_id for med_id, label in med_options if label == selected_med_label)
                
                # Get medication details for display
                med_details = df_m[df_m['MedicationID'] == selected_med_id].iloc[0]
                frequency_amount = med_details.get('FrequencyAmount', 1) or 1
                
                # Confirmation checkbox OUTSIDE the form so it triggers a rerun when toggled
                confirm_key = f"confirm_admin_{selected_pid}_{selected_med_id}"
                done_key = f"admin_done_{selected_pid}_{selected_med_id}"
                confirm_admin = st.checkbox(
                    f"I confirm administration (will decrease refills by {frequency_amount})",
                    key=confirm_key,
                    help=f"This action will decrease the refill count by {frequency_amount}"
                )
                already_done = st.session_state.get(done_key, False)
                if already_done:
                    st.info("This medication has been recorded as administered for this selection.")

                # Administration form
                with st.form("administer_medication"):
                    st.markdown("### 📋 Administration Details")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="medical-card">
                            <strong>Medication:</strong> {med_details.get('PrescriptionName', 'Unknown')}<br>
                            <strong>Dosage:</strong> {med_details.get('DosageAmount', '')} {med_details.get('DosageUnit', '')}<br>
                            <strong>Frequency:</strong> {frequency_amount} {med_details.get('FrequencyPeriod', '')}
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="medical-card">
                            <strong>Current Refills:</strong> {med_details.get('RefillsLeft', 0)}<br>
                            <strong>Refills After Admin:</strong> {max(0, (med_details.get('RefillsLeft', 0) or 0) - frequency_amount)}<br>
                            <strong>Pickup Location:</strong> {med_details.get('PickUpLocation', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)

                    # Submit button disabled after first successful submission
                    if st.form_submit_button("Administered Medication", type="primary", disabled=already_done):
                        if not confirm_admin:
                            st.error("Please confirm administration using the checkbox above.")
                        else:
                            success, message = administer_medication(selected_pid, selected_med_id)
                            if success:
                                st.session_state[done_key] = True
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(f"Failed to administer medication: {message}")
        else:
            st.info("No medications available for administration (all medications have 0 refills).")
    else:
        st.info("No medications found for this patient.")


