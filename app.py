import streamlit as st

from src.start_end import render_start_page, render_end_page
from src.control import render_control_group
from src.friction import render_friction_nudge
from src.disclosure import render_disclosure_nudge
from src.feedback import render_feedback_nudge
from src.prescreening import render_prescreening
from src.session import init
from src.storage import save_to_google_sheets


if __name__ == "__main__":
    init()

    # 1. Check if the study is finished first
    if st.session_state.study_completed:
        if not st.session_state.get('data_saved', False):
            save_to_google_sheets()
            st.session_state.data_saved = True
        render_end_page()

    # 2. Check if we haven't started yet
    elif "study_started" not in st.session_state:
        render_start_page()

    # 3. Check if we are still in prescreening
    elif "prescreening_complete" not in st.session_state and st.session_state.study_started:
        render_prescreening()

    # 4. Finally, if everything else is done, render the main study
    elif st.session_state.study_started and st.session_state.prescreening_complete:
        nudge_type = st.session_state.nudge

        st.caption("You are participating in a study on decision-making. Your responses will be used for research purposes.")
        
        if nudge_type == "control":
            render_control_group()
        elif nudge_type == "friction":
            render_friction_nudge()
        elif nudge_type == "feedback":
            render_feedback_nudge()
        elif nudge_type == "disclosure":
            render_disclosure_nudge()
        else:
            render_control_group()
