import streamlit as st
import time
import json
import gspread
from google.oauth2.service_account import Credentials

def save_response_data(current_task, response, used_alternative_search):
    """Save response data in a structured format for easy export."""
    response_data = {
        "participant_id": st.session_state.participant_id,
        "nudge_type": st.session_state.nudge,
        "task_index": st.session_state.task_index,
        "task_id": current_task['task_id'],
        "task_complexity": current_task['complexity'],
        "prompt": response,
        "used_alternative_search": used_alternative_search,
        "timestamp": time.time(),
        "timestamp_readable": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    
    st.session_state.responses.append(response_data)


def export_to_json():
    """Export all responses to a structured JSON format."""
    export_data = {
        "study_metadata": {
            "participant_id": st.session_state.participant_id,
            "nudge_type": st.session_state.nudge,
            "total_tasks": len(st.session_state.tasks),
            "completed_tasks": len(st.session_state.responses),
            "completion_time": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "responses": st.session_state.responses,
    }
    return json.dumps(export_data, indent=2)


def export_to_csv_format():
    """Export responses in a flat format suitable for Google Sheets."""
    # Create a flat list for each response
    rows = []
    for response in st.session_state.responses:
        
        
        row = {
            "participant_id": response["participant_id"],
            "nudge_type": response["nudge_type"],
            "task_index": response["task_index"],
            "task_id": response["task_id"],
            "task_complexity": response["task_complexity"],
            "prompt": response["prompt"],
            "used_alternative_search": response["used_alternative_search"],
            "timestamp": response["timestamp"],
            "timestamp_readable": response["timestamp_readable"],
        }
        rows.append(row)
    
    return rows

def save_google_sheets(row_data):
    try:
            
            secrets = st.secrets["connections"]["gsheets"]
            
            
            creds = Credentials.from_service_account_info(
                secrets,
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
            )
            client = gspread.authorize(creds)
            
            
            spreadsheet = client.open_by_url(secrets["spreadsheet"])
            worksheet = spreadsheet.sheet1 # Targets the first tab
            
        
            worksheet.append_row(row_data)
            
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
