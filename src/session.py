import streamlit as st
import random
import json
import uuid

@st.cache_data
def load_tasks():
    with open("tasks.json", "r") as f:
        return json.load(f)["tasks"]
    

def init():

    # Initialize session state
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    if "task_index" not in st.session_state:
        st.session_state.task_index = 0

    if "participant_id" not in st.session_state:
        st.session_state.participant_id = str(uuid.uuid4())

    if "nudge" not in st.session_state:
        st.session_state.nudge = random.choice([
            "control",
            "friction",
            "default",
            "feedback"
        ])

    if "last_submit_time" not in st.session_state:
        st.session_state.last_submit_time = None

    if "responses" not in st.session_state:
        st.session_state.responses = []

    if "study_started" not in st.session_state:
        st.session_state.study_started = False

    if "study_completed" not in st.session_state:
        st.session_state.study_completed = False

    if "show_transition" not in st.session_state:
        st.session_state.show_transition = False

    if "transition_start_time" not in st.session_state:
        st.session_state.transition_start_time = None