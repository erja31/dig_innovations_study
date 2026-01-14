import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import structlog

logger = structlog.get_logger(name=__name__)
def save_response_data(current_task, response, used_alternative_search):
    """Save response data as a list for easy export."""
    # Store as list in the correct order
    response_data = [
        st.session_state.participant_id,
        st.session_state.nudge,
        st.session_state.task_index,
        current_task['task_id'],
        current_task['complexity'],
        response,
        used_alternative_search,
        datetime.now().isoformat(),
    ]
    
    st.session_state.responses.append(response_data)
    return response_data  # Return for use in Google Sheets





def save_to_google_sheets():
    """Save a single response row to Google Sheets."""
    try:
        # Get credentials from Streamlit secrets
        secrets = st.secrets["connections"]["gsheets"]
        
        # Create credentials
        creds = Credentials.from_service_account_info(
            secrets,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        
        client = gspread.authorize(creds)
        # Open spreadsheet
        spreadsheet = client.open_by_url(secrets["spreadsheet"])
        worksheet = spreadsheet.worksheet("MainStudy") 
    
        for response in st.session_state.responses:
            
            worksheet.append_row(response)
    
        
        
        return True
        
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
        logger.info("Error saving to Google Sheets", exception=str(e))
        return False