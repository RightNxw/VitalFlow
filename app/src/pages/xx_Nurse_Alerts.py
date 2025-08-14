import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from modules.nav import SideBarLinks


st.set_page_config(page_title="Nurse Alerts", page_icon="🚨", layout="wide")

# Sidebar navigation
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
    # Auto-detect container vs local host
    if os.path.exists('/.dockerenv'):
        API_BASE = "http://web-api:4000"
    else:
        API_BASE = "http://localhost:4000"
if DEFAULT_NURSE_ID == 0:
    DEFAULT_NURSE_ID = 2


def list_alerts(nurse_id: int):
    try:
        r = requests.get(
            f"{API_BASE}/alert/?user_type=nurse&user_id={nurse_id}", timeout=10
        )
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


def ack_alert(alert_id: int, nurse_id: int):
    try:
        r = requests.put(
            f"{API_BASE}/alert/{alert_id}",
            json={"user_type": "nurse", "user_id": nurse_id},
            timeout=10,
        )
        if r.status_code != 200:
            st.error(f"PUT /alert/{alert_id} → {r.status_code}")
            return False
        return True
    except requests.exceptions.RequestException as ex:
        st.error(f"Acknowledge failed at {API_BASE}. Details: {ex}")
        return False


def create_alert(payload: dict):
    try:
        r = requests.post(f"{API_BASE}/alert/", json=payload, timeout=10)
        if r.status_code not in (200, 201):
            st.error(f"POST /alert/ → {r.status_code}")
            return None
        return r.json()
    except requests.exceptions.RequestException as ex:
        st.error(f"Create alert failed at {API_BASE}. Details: {ex}")
        return None


st.title("Alerts")

# Load data
alerts = list_alerts(DEFAULT_NURSE_ID)
df = pd.DataFrame(alerts)
if not df.empty:
    if "SentTime" in df.columns:
        df["SentTime"] = pd.to_datetime(df["SentTime"], errors="coerce")
    if "UrgencyLevel" in df.columns:
        df = df.sort_values(by=["UrgencyLevel", "SentTime"], ascending=[False, False])

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
            if ack_alert(int(selected_id), DEFAULT_NURSE_ID):
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
                    "PostedBy": DEFAULT_NURSE_ID,
                    "PostedByRole": "Nurse",  # Hardcoded since we know it's a nurse
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
            st.info(detail.get("Message", "-"))
            st.write("Protocol:")
            st.code(detail.get("Protocol", "-"))
else:
    st.caption("No alert selected. Choose one from the table above.")


