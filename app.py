import streamlit as st
import time

from src.start_end import render_start_page, render_end_page
from src.control import render_control_group
from src.friction import render_friction_nudge
from src.disclosure import render_disclosure_nudge
from src.feedback import render_feedback_nudge
from src.session import init



def render_transition_screen():
    """Render a brief transition screen between tasks."""
    st.title("Task Completed! ✓")
    
    current_task_num = st.session_state.task_index
    total_tasks = len(st.session_state.tasks)
    
    st.success(f"### Task {current_task_num} completed successfully!")
    
    # Progress bar
    progress = current_task_num / total_tasks
    st.progress(progress)
    st.write(f"Progress: {current_task_num}/{total_tasks} tasks completed")
    
    st.markdown("---")
    st.info("Preparing next task...")
    
    # Auto-advance after 2 seconds
    if st.session_state.transition_start_time is None:
        st.session_state.transition_start_time = time.time()
    
    elapsed = time.time() - st.session_state.transition_start_time
    
    if elapsed < 3:
        # Show countdown or just wait
        remaining = int(3 - elapsed)
        st.write(f"Starting in {remaining + 1} seconds...")
        time.sleep(0.5)
        st.rerun()
    else:
        # Transition complete, move to next task
        st.session_state.show_transition = False
        st.session_state.transition_start_time = None
        st.rerun()

if __name__ == "__main__":
    init()

    if not st.session_state.study_started:
        render_start_page()
    elif st.session_state.study_completed:
        render_end_page()
    elif st.session_state.show_transition:
        render_transition_screen()
    else:
        nudge_type = st.session_state.nudge

        st.caption("You are participating in a study on decision-making. Your responses will be used for research purposes.")
        
        if nudge_type == "control":
            render_control_group()
        elif nudge_type == "friction":
            render_friction_nudge()
        elif nudge_type == "feedback":
            render_feedback_nudge()
        elif nudge_type == "default":
            render_disclosure_nudge()
        else:
            render_control_group()