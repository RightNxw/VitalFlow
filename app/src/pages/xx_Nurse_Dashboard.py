import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
from modules.nav import SideBarLinks

st.set_page_config(page_title="Nurse Dashboard", page_icon="👩‍⚕️", layout="wide")

API_BASE = os.getenv("API_BASE")
DEFAULT_NURSE_ID = int(os.getenv("DEFAULT_NURSE_ID", "0") or 0)
try:
    from modules.config import API_BASE as CFG_API_BASE, DEFAULT_NURSE_ID as CFG_NURSE_ID
    API_BASE = API_BASE or CFG_API_BASE
    DEFAULT_NURSE_ID = DEFAULT_NURSE_ID or int(CFG_NURSE_ID)
except Exception:
    pass
if not API_BASE:
    # Auto-detect container vs local host
    if os.path.exists('/.dockerenv'):
        API_BASE = "http://web-api:4000"
    else:
        API_BASE = "http://localhost:4000"
if DEFAULT_NURSE_ID == 0:
    DEFAULT_NURSE_ID = 1

def get_alerts(nurse_id: int):
    try:
        r = requests.get(f"{API_BASE}/alert/?user_type=nurse&user_id={nurse_id}", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /alert/ → {r.status_code}")
            return []
        return r.json() or []
    except requests.exceptions.RequestException as ex:
        st.error(f"Alerts service unreachable at {API_BASE}. Details: {ex}")
        return []

def get_alert(alert_id: int):
    try:
        r = requests.get(f"{API_BASE}/alert/{alert_id}", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /alert/{alert_id} → {r.status_code}")
            return None
        return r.json()
    except requests.exceptions.RequestException as ex:
        st.error(f"Alert detail unreachable at {API_BASE}. Details: {ex}")
        return None

def put_alert_ack(alert_id: int, nurse_id: int):
    try:
        r = requests.put(f"{API_BASE}/alert/{alert_id}", json={"user_type": "nurse", "user_id": nurse_id}, timeout=10)
        if r.status_code != 200:
            st.error(f"PUT /alert/{alert_id} → {r.status_code}")
            return False
        return True
    except requests.exceptions.RequestException as ex:
        st.error(f"Acknowledge failed at {API_BASE}. Details: {ex}")
        return False

def post_alert(payload: dict):
    try:
        r = requests.post(f"{API_BASE}/alert/", json=payload, timeout=10)
        if r.status_code not in (200, 201):
            st.error(f"POST /alert/ → {r.status_code}")
            return None
        return r.json()
    except requests.exceptions.RequestException as ex:
        st.error(f"Create alert failed at {API_BASE}. Details: {ex}")
        return None

def get_patients():
    try:
        r = requests.get(f"{API_BASE}/patient/", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /patient/ → {r.status_code}")
            return []
        return r.json() or []
    except requests.exceptions.RequestException as ex:
        st.error(f"Patients service unreachable at {API_BASE}. Details: {ex}")
        return []

SideBarLinks()

st.title("Nurse Dashboard")

# Load data
alerts = list_alerts(DEFAULT_NURSE_ID) if (refresh or True) else []
patients = get_patients()

df_alerts = pd.DataFrame(alerts)
if not df_alerts.empty:
    df_alerts["SentTime"] = pd.to_datetime(df_alerts.get("SentTime", None), errors="coerce")
    df_alerts = df_alerts.sort_values(by=["UrgencyLevel", "SentTime"], ascending=[False, False])

with st.container():
    c1, c2, c3, c4 = st.columns(4)
    total_alerts = len(df_alerts) if not df_alerts.empty else 0
    high_urg = int((df_alerts["UrgencyLevel"] >= 4).sum()) if not df_alerts.empty and "UrgencyLevel" in df_alerts else 0
    last_alert_time = df_alerts["SentTime"].max() if not df_alerts.empty and "SentTime" in df_alerts else None
    my_patients = [p for p in patients if str(p.get("NurseID", "")) == str(DEFAULT_NURSE_ID)]
    c1.metric("Alerts", total_alerts)
    c2.metric("High urgency (≥4)", high_urg)
    c3.metric("My patients", len(my_patients))
    c4.metric("Last alert", "-" if not last_alert_time else last_alert_time.strftime("%Y-%m-%d %H:%M"))

st.divider()

# Controls row
ctrl_l, ctrl_r = st.columns([3, 1])
with ctrl_l:
    auto_refresh = st.checkbox("Auto refresh", value=False)
    refresh = st.button("Refresh")
with ctrl_r:
    pass  # Removed NurseID input since we know which nurse is logged in

lc, rc = st.columns([2, 1])

with lc:
    st.subheader("Live Alerts")
    filter_col1, filter_col2 = st.columns([3, 1])
    q = filter_col1.text_input("Search", "")
    urg = filter_col2.selectbox("Urgency", ["All", "5", "4", "3", "2", "1"], index=0)
    view = df_alerts.copy() if not df_alerts.empty else pd.DataFrame()
    if not view.empty and q:
        ql = q.lower()
        cols = [c for c in ["Message", "Protocol", "PostedBy", "PostedByRole"] if c in view.columns]
        if cols:
            view = view[view[cols].astype(str).apply(lambda r: any(ql in str(x).lower() for x in r), axis=1)]
    if not view.empty and urg != "All" and "UrgencyLevel" in view.columns:
        view = view[view["UrgencyLevel"] == int(urg)]
    show_cols = [c for c in ["AlertID", "UrgencyLevel", "Message", "Protocol", "PostedBy", "SentTime"] if c in view.columns]
    st.dataframe(view[show_cols] if not view.empty else pd.DataFrame(columns=["AlertID","UrgencyLevel","Message","Protocol","PostedBy","SentTime"]), use_container_width=True, hide_index=True)
    sel_id = st.text_input("Select AlertID to view/ack", value=str(int(view["AlertID"].iloc[0])) if not view.empty and "AlertID" in view.columns else "0")
    cc1, cc2 = st.columns(2)
    with cc1:
        if st.button("View Selected", disabled=(int(sel_id) <= 0)):
            st.session_state["selected_alert_id"] = int(sel_id)
    with cc2:
        if st.button("Acknowledge Selected", type="primary", disabled=(int(sel_id) <= 0)):
            ok = put_alert_ack(int(sel_id), DEFAULT_NURSE_ID)
            if ok:
                st.success("Acknowledged")
                st.rerun()

with rc:
    st.subheader("Create Alert")
    with st.form("create_alert"):
        msg = st.text_area("Message", "")
        urg_val = st.slider("UrgencyLevel", 1, 5, 3)
        proto = st.text_area("Protocol", "")
        posted_by_id = st.text_input("PostedBy (NurseID)", value=str(DEFAULT_NURSE_ID))
        submit = st.form_submit_button("Create")
        if submit:
            if not msg.strip():
                st.error("Message required")
            else:
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                res = post_alert({
                    "Message": msg.strip(),
                    "SentTime": now_str,
                    "PostedBy": int(posted_by_id),
                    "PostedByRole": "Nurse",  # Hardcoded since we know it's a nurse
                    "UrgencyLevel": int(urg_val),
                    "Protocol": proto.strip()
                })
                if res is not None:
                    st.success("Alert created")
                    st.rerun()

st.divider()

st.subheader("Selected Alert")
sel_alert_id = st.session_state.get("selected_alert_id", 0)
if sel_alert_id:
    detail = get_alert(int(sel_alert_id))
    if detail:
        st.json(detail, expanded=False)
else:
    st.caption("Select an alert in the table to view details")

st.divider()

st.subheader("My Patients")
mp = pd.DataFrame(my_patients)
if mp.empty:
    st.write("No assigned patients.")
else:
    cols = [c for c in ["PatientID","FirstName","LastName","DOB","ConditionID","DoctorID","NurseID"] if c in mp.columns]
    st.dataframe(mp[cols], use_container_width=True, hide_index=True)
