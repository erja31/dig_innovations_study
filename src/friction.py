import streamlit as st
import time
from src.storage import save_response_data

def render_friction_nudge():
    st.title("Chat Interface")
    current_task = st.session_state.tasks[st.session_state.task_index]

    st.markdown(f"### Task {current_task['task_id']}")
    st.write(f"**Complexity:** {current_task['complexity']}")
    st.write(current_task["prompt"])

    response = st.text_area("Your response", key=f"response_{st.session_state.task_index}")

    COOLDOWN_SECONDS = 10
    button_disabled = False
    time_remaining = 0
    cooldown_expired = False

    # Disable button if response is empty
    if not response.strip():
        button_disabled = True

    # Check if we're still in cooldown period
    if st.session_state.last_submit_time and response.strip():
        elapsed = time.time() - st.session_state.last_submit_time
        if elapsed < COOLDOWN_SECONDS:
            button_disabled = True
            time_remaining = int(COOLDOWN_SECONDS - elapsed) + 1
        else:
            # Cooldown has expired
            cooldown_expired = True

    # Show warning if still in cooldown
    if button_disabled and st.session_state.last_submit_time and response.strip():
        st.warning(f"⏳ Please wait {time_remaining} seconds before submitting. Use this time to reconsider your response. Keep in mind that shorter and more concise prompts use significantly less energy and a switch to a standard Google search can use up to 10 times less energy than the usage of a LLM!")
        time.sleep(1)
        st.rerun()

    col1, col2 = st.columns(2)
    
    with col1:
        submitted = st.button("Submit", disabled=button_disabled, key=f"submit_{st.session_state.task_index}", type="primary", use_container_width=True)
    
    with col2:
        alt_search = st.button(
            "🌱 Search Elsewhere",
            key=f"alt_search_{st.session_state.task_index}",
            help="Use a more sustainable search engine like Ecosia",
            use_container_width=True
        )

    if alt_search:
        save_response_data(current_task, response, used_alternative_search=True)
        
        # Move to next task
        if st.session_state.task_index < len(st.session_state.tasks) - 1:
            st.session_state.task_index += 1
            st.session_state.show_transition = True
            st.rerun()
        else:
            st.session_state.study_completed = True
            st.rerun()

    elif submitted and response.strip():
        if cooldown_expired:
            # Cooldown just expired, now actually submit
            
            st.success("Response submitted!")
            save_response_data(current_task, response, used_alternative_search=False)
        
            
            # Reset for next task
            st.session_state.last_submit_time = None
            time.sleep(1)
            
            # Move to next task
            if st.session_state.task_index < len(st.session_state.tasks) - 1:
                st.session_state.task_index += 1
                st.session_state.show_transition = True
                st.rerun()
            else:
                st.session_state.study_completed = True
                st.rerun()
                
        elif st.session_state.last_submit_time is None:
            # First click - start the cooldown
            st.session_state.last_submit_time = time.time()
            st.rerun()