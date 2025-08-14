import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from modules.nav import SideBarLinks


st.set_page_config(page_title="Nurse Patients", page_icon="🧑‍🤝‍🧑", layout="wide")

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


st.title("Patients")

ctrl_l, ctrl_r = st.columns([3, 1])
with ctrl_l:
    q = st.text_input("Search name, blood type…")
    only_mine = st.checkbox("Only my patients", value=True)
    refresh = st.button("Refresh")
with ctrl_r:
    nurse_id = st.number_input("NurseID", min_value=1, step=1, value=int(DEFAULT_NURSE_ID))

patients = list_patients() if (refresh or True) else []
df = pd.DataFrame(patients)
if not df.empty:
    # Filters
    if only_mine and "NurseID" in df.columns:
        df = df[df["NurseID"].astype(str) == str(int(nurse_id))]
    if q:
        ql = q.lower()
        cols = [c for c in ["FirstName", "LastName", "BloodType"] if c in df.columns]
        if cols:
            df = df[df[cols].astype(str).apply(lambda r: any(ql in str(x).lower() for x in r), axis=1)]
    sort_cols = [c for c in ["LastName", "FirstName", "PatientID"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(by=sort_cols)

left, right = st.columns([2, 1])

with left:
    st.subheader("Patient List")
    show_cols = [c for c in [
        "PatientID", "FirstName", "LastName", "DOB", "BloodType", "PreExisting",
        "ConditionID", "DoctorID", "NurseID", "VisitID", "VitalID"
    ] if c in df.columns]
    st.dataframe(df[show_cols] if not df.empty else pd.DataFrame(columns=show_cols), use_container_width=True, hide_index=True)

    sel_default = int(df["PatientID"].iloc[0]) if not df.empty and "PatientID" in df.columns else 0
    selected_id = st.number_input("Select PatientID", min_value=0, step=1, value=sel_default)
    if st.button("Open") and selected_id > 0:
        st.session_state["selected_patient_id"] = int(selected_id)
        st.rerun()

with right:
    st.subheader("Quick Details")
    pid = st.session_state.get("selected_patient_id", 0)
    if pid:
        p = get_patient(int(pid))
        v = get_patient_vitals(int(pid))
        c = get_patient_condition(int(pid))
        if p:
            st.write(f"PatientID: {p.get('PatientID', '-')}")
            st.write(f"Name: {p.get('FirstName', '')} {p.get('LastName', '')}")
            st.write(f"DOB: {p.get('DOB', '-')}")
            st.write(f"BloodType: {p.get('BloodType', '-')}")
        if v:
            st.markdown("**Vitals**")
            st.write(f"HR: {v.get('HeartRate', '-')}")
            st.write(f"BP: {v.get('BloodPressure', '-')}")
            st.write(f"RR: {v.get('RespiratoryRate', '-')}")
            st.write(f"Temp: {v.get('Temperature', '-')}")
        if c:
            st.markdown("**Condition**")
            st.write(c.get("Description", "-"))
            st.code(c.get("Treatment", "-"))
    else:
        st.caption("Select a patient to view details")


