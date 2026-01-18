import streamlit as st
import time
import pandas as pd

def render_start_page():
    """Render the initial study information and consent page."""
    st.title("🔬 Welcome to Our Research Study")
    
    st.markdown("""
    ## Study Information
    
    Thank you for your interest in participating in our research study on **sustainable information systems**.
    
    
    ### What You'll Do
    - Complete **12 tasks** that involve writing prompts for an AI chatbot
    - Each task presents a scenario where you need to formulate a prompt to get the desired information
    - The interface may provide different types of guidance or feedback
    - Your responses will be recorded for research purposes
    
    ### Time Commitment
    The study takes approximately **10-15 minutes** to complete.
    
    ### Privacy & Data
    - Your responses are **anonymous** and will be used only for research purposes
    - A random participant ID has been assigned to you: `{}`
    - No personally identifiable information will be collected
    - You may withdraw from the study at any time
    
    ### Consent
    By clicking confirming below, you acknowledge that:
    - You have read and understood the study information
    - You voluntarily agree to participate
    - You understand your data will be used for research purposes
    
    ---
    
    If you have any questions about this study, please contact the research team before proceeding.
    """.format(st.session_state.participant_id))

    if st.checkbox("I have read and agree to the terms of the study.", key="consent_checkbox"):
        disabled = False
    else:
        disabled = True
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(label="Start Study", type="primary", disabled=disabled, use_container_width=True):
            st.session_state.study_started = True
            st.rerun()


def render_end_page():
    """Render the final thank you page after study completion."""
    st.balloons()
    
    st.title("🎉 Study Complete!")
    
    st.success("### Thank you for your participation!")
    
    st.markdown("""
    ## Your Contribution Matters
    
    Your responses have been successfully recorded and will contribute to our research on 
    sustainable information systems.
    
    ### What Happens Next?
    - Your anonymous data will be analyzed alongside other participants' responses
    - The findings will help improve AI interface design
    - Results may be published in academic journals or conferences
    
    ### Study Details
    - **Participant ID:** `{}`
    - **Nudge Type:** {}
    - **Completion Time:** {}
    
    ### Questions or Concerns?
    If you have any questions about the study or would like to learn more about the research, 
    please feel free to contact us. 
                
    
    ---
    
    You may now close this window.
    """.format(
        st.session_state.participant_id,
        st.session_state.nudge,
        time.strftime("%Y-%m-%d %H:%M:%S")
    ))
