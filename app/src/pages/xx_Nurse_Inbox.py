import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from modules.nav import SideBarLinks


st.set_page_config(page_title="Nurse Inbox", page_icon="📥", layout="wide")

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


def list_messages(nurse_id: int):
    try:
        r = requests.get(
            f"{API_BASE}/messages",
            params={"user_type": "nurse", "user_id": nurse_id},
            timeout=10,
        )
        if r.status_code != 200:
            st.error(f"GET /messages → {r.status_code}")
            return []
        return r.json() or []
    except requests.exceptions.RequestException as ex:
        st.error(f"Messages service unreachable at {API_BASE}. Details: {ex}")
        return []


def get_message(message_id: int):
    try:
        r = requests.get(f"{API_BASE}/messages/{message_id}", timeout=10)
        if r.status_code != 200:
            st.error(f"GET /messages/{message_id} → {r.status_code}")
            return None
        return r.json()
    except requests.exceptions.RequestException as ex:
        st.error(f"Message detail unreachable at {API_BASE}. Details: {ex}")
        return None


def create_message(payload: dict):
    try:
        r = requests.post(f"{API_BASE}/messages", json=payload, timeout=10)
        if r.status_code not in (200, 201):
            st.error(f"POST /messages → {r.status_code}")
            return None
        return r.json()
    except requests.exceptions.RequestException as ex:
        st.error(f"Create message failed at {API_BASE}. Details: {ex}")
        return None


st.title("Inbox")

top_l, top_r = st.columns([3, 1])
with top_l:
    q = st.text_input("Search")
    refresh = st.button("Refresh")
with top_r:
    nurse_id = st.number_input("NurseID", min_value=1, step=1, value=int(DEFAULT_NURSE_ID))

messages = list_messages(int(nurse_id)) if (refresh or True) else []
df = pd.DataFrame(messages)
if not df.empty:
    if "SentTime" in df.columns:
        df["SentTime"] = pd.to_datetime(df["SentTime"], errors="coerce")
    df = df.sort_values(by=["SentTime"], ascending=[False])

left, right = st.columns([2, 1])

with left:
    st.subheader("Messages")
    view = df.copy() if not df.empty else pd.DataFrame()
    if not view.empty and q:
        ql = q.lower()
        cols = [c for c in ["Message", "PostedBy", "PostedByRole"] if c in view.columns]
        if cols:
            view = view[view[cols].astype(str).apply(lambda r: any(ql in str(x).lower() for x in r), axis=1)]
    cols = [c for c in ["MessageID", "SentTime", "PostedBy", "PostedByRole", "Message"] if c in view.columns]
    st.dataframe(view[cols] if not view.empty else pd.DataFrame(columns=cols), use_container_width=True, hide_index=True)

    sel_default = int(view["MessageID"].iloc[0]) if not view.empty and "MessageID" in view.columns else 0
    selected_id = st.number_input("Select MessageID", min_value=0, step=1, value=sel_default)
    if st.button("Open") and selected_id > 0:
        st.session_state["selected_message_id"] = int(selected_id)
        st.rerun()

with right:
    st.subheader("Compose Handover Note")
    with st.form("compose"):
        body = st.text_area("Message")
        role = st.text_input("PostedByRole", "nurse")
        submit = st.form_submit_button("Send")
        if submit:
            if not body.strip():
                st.error("Message required")
            else:
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                res = create_message({
                    "Message": body.strip(),
                    "SentTime": now_str,
                    "PostedBy": int(nurse_id),
                    "PostedByRole": role.strip() or "nurse",
                })
                if res is not None:
                    st.success("Message created")
                    st.rerun()

st.divider()

st.subheader("Selected Message")
sel_msg_id = st.session_state.get("selected_message_id", 0)
if sel_msg_id:
    detail = get_message(int(sel_msg_id))
    if detail:
        st.write(f"MessageID: {detail.get('MessageID', '-')}")
        st.write(f"Sent: {detail.get('SentTime', '-')}")
        st.write(f"PostedBy: {detail.get('PostedBy', '-')}")
        st.write(f"Role: {detail.get('PostedByRole', '-')}")
        st.write("Message:")
        st.info(detail.get("Message", "-"))
else:
    st.caption("No message selected. Choose one from the table above.")


