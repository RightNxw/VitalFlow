import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from modules.nav import SideBarLinks


st.set_page_config(page_title="Nurse Treatments", page_icon="💊", layout="wide")

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
        r = requests.get(f"{API_BASE}/patient/patients", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /patient/patients → {r.status_code}")
            return []
        return r.json() or []
    except requests.exceptions.RequestException as ex:
        st.error(f"Patients service unreachable at {API_BASE}. Details: {ex}")
        return []


def get_patient(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/patients/{pid}", timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


def get_patient_medications(pid: int):
    try:
        r = requests.get(f"{API_BASE}/patient/patients/{pid}/medications", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /patient/patients/{pid}/medications → {r.status_code}")
            return []
        return r.json() or []
    except requests.exceptions.RequestException as ex:
        st.error(f"Medications service unreachable at {API_BASE}. Details: {ex}")
        return []


st.title("Treatments")

top_l, top_r = st.columns([3, 1])
with top_l:
    only_mine = st.checkbox("Only my patients", value=True)
    refresh = st.button("Refresh")
with top_r:
    nurse_id = st.number_input("NurseID", min_value=1, step=1, value=int(DEFAULT_NURSE_ID))

patients = list_patients() if (refresh or True) else []
df_pat = pd.DataFrame(patients)
if only_mine and not df_pat.empty and "NurseID" in df_pat.columns:
    df_pat = df_pat[df_pat["NurseID"].astype(str) == str(int(nurse_id))]

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
    st.subheader("Patient Summary")
    if p:
        st.write(f"PatientID: {p.get('PatientID','-')}")
        st.write(f"Name: {p.get('FirstName','')} {p.get('LastName','')}")
        st.write(f"DOB: {p.get('DOB','-')}  •  BloodType: {p.get('BloodType','-')}")

    st.divider()
    st.subheader("Current Prescriptions")
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
        st.caption("No medications linked to this patient.")

    st.divider()
    st.subheader("Log Administration: TODO")
    st.info("TODO: API route to record administrations isn't present yet.")


