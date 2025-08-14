
## doctor alerts page

import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.styles import apply_page_styling, create_metric_card, create_medical_divider

## Apply medical theme and styling
apply_page_styling()

## Add logo and navigation
SideBarLinks()

## Page config

# Medical-themed header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">⚠️ Patient Alerts</h1>
    <p style="font-size: 1.2rem; color: var(--gray-600); margin: 0;">
        View and manage patient alerts
    </p>
</div>
""", unsafe_allow_html=True)

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

# Load data
alerts = get_alerts(doctor_id)
df = pd.DataFrame(alerts)
if not df.empty:
    if "SentTime" in df.columns:
        df["SentTime"] = pd.to_datetime(df["SentTime"], errors="coerce")
    if "UrgencyLevel" in df.columns:
        df = df.sort_values(by=["UrgencyLevel", "SentTime"], ascending=[False, False])

# Dashboard metrics
metric_1, metric_2, metric_3 = st.columns(3)
metric_1.markdown(create_metric_card("Total Alerts", len(df) if not df.empty else 0, "📊"), unsafe_allow_html=True)
metric_2.markdown(create_metric_card("High Urgency (≥4)", int((df["UrgencyLevel"] >= 4).sum()) if not df.empty and "UrgencyLevel" in df.columns else 0, "⚠️"), unsafe_allow_html=True)
metric_3.markdown(create_metric_card("Last Alert", "-" if df.empty or "SentTime" not in df.columns else df["SentTime"].max().strftime("%Y-%m-%d %H:%M"), "🕐"), unsafe_allow_html=True)

st.markdown(create_medical_divider(), unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown("### 📊 Live Feed")
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
        if st.button("View", use_container_width=True, type="primary"):
            if int(selected_id) > 0:
                st.session_state["selected_alert_id"] = int(selected_id)
                st.rerun()
    with c2:
        if st.button("Acknowledge", type="primary", use_container_width=True, disabled=(int(selected_id) <= 0)):
            if ack_alert(int(selected_id), int(doctor_id)):
                st.success("Acknowledged")
                st.rerun()

with right:
    st.markdown("### ✨ Create Alert")
    with st.form("create_alert"):
        msg = st.text_area("Message", placeholder="Enter alert message...")
        urg_val = st.slider("Urgency Level", 1, 5, 3)
        proto = st.text_area("Protocol", placeholder="Enter protocol instructions...")
        submit = st.form_submit_button("Create Alert", type="primary", use_container_width=True)
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
                    st.success("Alert created successfully!")
                    st.rerun()

st.markdown(create_medical_divider(), unsafe_allow_html=True)

st.markdown("### 📋 Selected Alert Details")
sel_alert_id = st.session_state.get("selected_alert_id", 0)
if sel_alert_id:
    detail = get_alert(int(sel_alert_id))
    if detail:
        left_col, right_col = st.columns([1, 1])
        with left_col:
            st.markdown(f"""
            <div class="medical-card">
                <strong>Alert ID:</strong> {detail.get('AlertID', '-')}<br>
                <strong>Urgency:</strong> {detail.get('UrgencyLevel', '-')}<br>
                <strong>Sent:</strong> {detail.get('SentTime', '-')}<br>
                <strong>Posted By:</strong> {detail.get('PostedBy', '-')}<br>
                <strong>Role:</strong> {detail.get('PostedByRole', '-')}
            </div>
            """, unsafe_allow_html=True)
        with right_col:
            st.markdown(f"""
            <div class="medical-card">
                <strong>Message:</strong><br>
                {detail.get('Message', '-')}<br><br>
                <strong>Protocol:</strong><br>
                {detail.get('Protocol', '-')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Could not load alert details")
else:
    st.info("Select an alert in the table above to view details")
 