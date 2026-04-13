import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

def save_log(logs, session_id=None):
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    sheet = client.open("reflection_logs").sheet1
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for entry in logs:
        sheet.append_row([
            session_id or timestamp,
            entry["stage"],
            entry["user_input"],
            entry["verdict"],
            str(entry["fulfilled"]),
            str(entry["missing"]),
            entry["forced_advance"],
            entry["turn_in_stage"]
        ])