
## doctor alerts page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
 
## Add logo and navigation
SideBarLinks()
 
## Page config
st.write("# Patient Alerts")
st.write("View and manage patient alerts.")
 
## API configuration
API_BASE_URL = "http://web-api:4000"

## Constants
DEFAULT_DOCTOR_ID = 1

## API functions
def get_alerts(doctor_id):
    """Get alerts for specific doctor"""
    try:
        response = requests.get(f"{API_BASE_URL}/alert/?user_type=doctor&user_id={doctor_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        st.warning("Could not connect to alerts API, using dummy data.")
        return [
            {
                "AlertID": 1, 
                "Message": "Patient blood pressure critically high: 180/110", 
                "PostedBy": 2, 
                "PostedByRole": "Nurse", 
                "Protocol": "Immediate intervention required. Administer antihypertensive medication.", 
                "SentTime": "Thu, 14 Aug 2025 01:49:01 GMT", 
                "UrgencyLevel": 5
            }
        ]

def ack_alert(alert_id, doctor_id):
    """Acknowledge an alert"""
    try:
        response = requests.put(f"{API_BASE_URL}/alert/{alert_id}", 
                              json={"user_type": "doctor", "user_id": doctor_id})
        return response.status_code == 200
    except:
        return False

def create_alert(alert_data):
    """Create a new alert"""
    try:
        response = requests.post(f"{API_BASE_URL}/alert/", json=alert_data)
        return response.status_code == 201
    except:
        return False

def get_alert(alert_id):
    """Get specific alert details"""
    try:
        response = requests.get(f"{API_BASE_URL}/alert/{alert_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

## Get alerts for current doctor
doctor_id = st.session_state.get('current_doctor_id', DEFAULT_DOCTOR_ID)

# Controls row
ctrl_l, ctrl_r = st.columns([3, 1])
with ctrl_l:
    auto_refresh = st.checkbox("Auto refresh", value=False)
    refresh = st.button("Refresh")
with ctrl_r:
    pass  # Removed DoctorID input since we know which doctor is logged in

# Load data
alerts = get_alerts(int(doctor_id)) if (refresh or True) else []
df = pd.DataFrame(alerts)
if not df.empty:
    if "SentTime" in df.columns:
        df["SentTime"] = pd.to_datetime(df["SentTime"], errors="coerce")
    if "UrgencyLevel" in df.columns:
        df = df.sort_values(by=["UrgencyLevel", "SentTime"], ascending=[False, False])

# Dashboard metrics
metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Total alerts", len(df) if not df.empty else 0)
metric_2.metric(
    "High urgency (≥4)",
    int((df["UrgencyLevel"] >= 4).sum()) if not df.empty and "UrgencyLevel" in df.columns else 0,
)
metric_3.metric(
    "Last alert",
    "-" if df.empty or "SentTime" not in df.columns else df["SentTime"].max().strftime("%Y-%m-%d %H:%M"),
)

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("Live Feed")
    f1, f2 = st.columns([3, 1])
    query = f1.text_input("Search")
    urgency = f2.selectbox("Urgency", ["All", "5", "4", "3", "2", "1"], index=0)

    view = df.copy() if not df.empty else pd.DataFrame()
    if not view.empty and query:
        ql = query.lower()
        cols = [c for c in ["Message", "Protocol", "PostedBy", "PostedByRole"] if c in view.columns]
        if cols:
            view = view[view[cols].astype(str).apply(lambda r: any(ql in str(x).lower() for x in r), axis=1)]
    if not view.empty and urgency != "All" and "UrgencyLevel" in view.columns:
        view = view[view["UrgencyLevel"] == int(urgency)]

    display_cols = [c for c in ["AlertID", "UrgencyLevel", "Message", "Protocol", "PostedBy", "SentTime"] if c in view.columns]
    st.dataframe(
        view[display_cols] if not view.empty else pd.DataFrame(columns=display_cols),
        use_container_width=True,
        hide_index=True,
    )

    sel_default = int(view["AlertID"].iloc[0]) if not view.empty and "AlertID" in view.columns else 0
    selected_id = st.text_input("Select AlertID", value=str(sel_default))
    c1, c2 = st.columns(2)
    with c1:
        if st.button("View") and int(selected_id) > 0:
            st.session_state["selected_alert_id"] = int(selected_id)
            st.rerun()
    with c2:
        if st.button("Acknowledge", type="primary", disabled=(int(selected_id) <= 0)):
            if ack_alert(int(selected_id), int(doctor_id)):
                st.success("Acknowledged")
                st.rerun()

with right:
    st.subheader("Create Alert")
    with st.form("create_alert"):
        msg = st.text_area("Message")
        urg_val = st.slider("UrgencyLevel", 1, 5, 3)
        proto = st.text_area("Protocol", "")
        submit = st.form_submit_button("Create")
        if submit:
            if not msg.strip():
                st.error("Message required")
            else:
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                res = create_alert({
                    "Message": msg.strip(),
                    "SentTime": now_str,
                    "PostedBy": int(doctor_id),
                    "PostedByRole": "Doctor",  # Hardcoded since we know it's a doctor
                    "UrgencyLevel": int(urg_val),
                    "Protocol": proto.strip(),
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
        left_col, right_col = st.columns([1, 1])
        with left_col:
            st.write(f"AlertID: {detail.get('AlertID', '-')}")
            st.write(f"Urgency: {detail.get('UrgencyLevel', '-')}")
            st.write(f"Sent: {detail.get('SentTime', '-')}")
            st.write(f"PostedBy: {detail.get('PostedBy', '-')}")
            st.write(f"Role: {detail.get('PostedByRole', '-')}")
        with right_col:
            st.write("Message:")
            st.write(detail.get('Message', '-'))
            st.write("Protocol:")
            st.write(detail.get('Protocol', '-'))
    else:
        st.error("Could not load alert details")
else:
    st.caption("Select an alert in the table to view details")
 