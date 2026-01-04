import streamlit as st
import time
import pandas as pd
from src.storage import export_to_json, export_to_csv_format

def render_start_page():
    """Render the initial study information and consent page."""
    st.title("🔬 Welcome to Our Research Study")
    
    st.markdown("""
    ## Study Information
    
    Thank you for your interest in participating in our research study on **sustainable information systems**.
    
    ### Purpose of the Study
    This study investigates how different interface designs and feedback mechanisms influence how people 
    formulate prompts when interacting with AI chatbots. Your participation will help us understand 
    effective ways to encourage thoughtful and efficient AI usage.
    
    ### What You'll Do
    - Complete **3 tasks** that involve writing prompts for an AI chatbot
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
    By clicking "Start Study" below, you acknowledge that:
    - You have read and understood the study information
    - You voluntarily agree to participate
    - You are at least 18 years old
    - You understand your data will be used for research purposes
    
    ---
    
    If you have any questions about this study, please contact the research team before proceeding.
    """.format(st.session_state.participant_id))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Study", type="primary", use_container_width=True):
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
    - **Tasks Completed:** {}
    - **Nudge Type:** {}
    - **Completion Time:** {}
    
    ### Questions or Concerns?
    If you have any questions about the study or would like to learn more about the research, 
    please feel free to contact us.
    
    ---
    
    You may now close this window.
    """.format(
        st.session_state.participant_id,
        len(st.session_state.responses),
        st.session_state.nudge,
        time.strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    # Export options
    st.markdown("### 📥 Download Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export (complete data)
        json_data = export_to_json()
        st.download_button(
            label="📄 Download Complete Data (JSON)",
            data=json_data,
            file_name=f"study_data_{st.session_state.participant_id}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # CSV-friendly format
        csv_rows = export_to_csv_format()
        df = pd.DataFrame(csv_rows)
        csv_data = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Download for Google Sheets (CSV)",
            data=csv_data,
            file_name=f"study_data_{st.session_state.participant_id}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Show preview of data
    with st.expander("📋 Preview Your Data"):
        st.dataframe(df)