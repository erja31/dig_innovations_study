import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

def render_prescreening():
    st.title("Participant Prescreening")
    st.info("Please answer a few questions about yourself before we begin the experiment.")
    
    # --- Part 1: Personal Info ---
    st.subheader("1. Profile")
    age = st.number_input("Age", min_value=18, max_value=99, step=1, value=25)
    gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say", "Other"])
    
    profession = st.radio("Current Status", ["Student", "Professional", "Other"])
    
    # Conditional Input: Only show if Student
    field_of_study = ""
    if profession == "Student":
        common_fields = [
            "Computer Science / IT",
            "Business / Economics",
            "Engineering",
            "Psychology",
            "Medicine / Health Sciences",
            "Law",
            "Education",
            "Biology / Life Sciences",
            "Arts / Humanities",
            "Social Sciences",
            "Physics / Mathematics",
            "Communications / Media",
            "Political Science",
            "Design / Architecture",
            "History",
            "Other"
        ]
        
        selected_field = st.selectbox("Field of Study", common_fields)
        
        if selected_field == "Other":
            field_of_study = st.text_input("Please specify your field:")
        else:
            field_of_study = selected_field
    
    st.write("---")

    # --- Part 2: Frequency ---
    st.subheader("2. Usage Habits")
    
    q_freq = "How frequently do you use generative AI tools (e.g., ChatGPT, Gemini)?"
    opts_freq = ["Never", "Less than Monthly", "Monthly", "Weekly", "Daily", "Multiple times a day"]
    usage_freq = st.selectbox(q_freq, opts_freq)
    
    st.write("")
    st.write("")
    
    if st.button("Start Experiment", type="primary"):
        # Simple validation
        if profession == "Student" and field_of_study.strip() == "":
            st.error("Please enter your Field of Study.")
        else:
            save_prescreening(age, gender, profession, field_of_study, usage_freq)
            st.session_state.prescreening_complete = True
            st.rerun()


def save_prescreening(age, gender, profession, field, freq_usage):
    """Saves demographics to the 'Demographics' tab."""
    row_data = [
        st.session_state.participant_id,
        datetime.now().isoformat(),
        st.session_state.nudge,
        age, gender, profession, field,
        freq_usage
    ]

    try:
        secrets = st.secrets["connections"]["gsheets"]
        creds = Credentials.from_service_account_info(
            secrets,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(creds)
        
        spreadsheet = client.open_by_url(secrets["spreadsheet"])
        # Ensure you created this tab in your Google Sheet!
        worksheet = spreadsheet.worksheet("Prescreening")
        
        worksheet.append_row(row_data)
        
        
    except Exception as e:
        st.error(f"Error saving Prescreening: {e}")
        st.stop()

