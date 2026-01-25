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
    if 'tasks' not in st.session_state:
        # 1. Load your tasks from the JSON file
        with open('tasks.json', 'r') as f:
            data = json.load(f)
    
        # 2. Extract the actual LIST from the "tasks" key
        task_list = data["tasks"]
    
        # 3. Shuffle the list
        random.shuffle(task_list)
        
        # 4. Store the randomized list and the index
        st.session_state.tasks = task_list
        st.session_state.task_index = 1
        st.session_state.study_completed = False

    if "participant_id" not in st.session_state:
        st.session_state.participant_id = str(uuid.uuid4())

    if "nudge" not in st.session_state:
        st.session_state.nudge = random.choice([
            "control",
            "friction",
            "disclosure",
        ])

    if "last_submit_time" not in st.session_state:
        st.session_state.last_submit_time = None

    if "responses" not in st.session_state:
        st.session_state.responses = []

    if "study_completed" not in st.session_state:
        st.session_state.study_completed = False

    if "data_saved" not in st.session_state:
        st.session_state.data_saved = False

    if "example_complete" not in st.session_state:
        st.session_state.example_complete = False