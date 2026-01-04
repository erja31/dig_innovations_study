import streamlit as st
import time
from src.storage import save_response_data

def render_disclosure_nudge():
    st.title("Chat Interface")
    current_task = st.session_state.tasks[st.session_state.task_index]

    st.markdown(f"### Task {current_task['task_id']}")
    st.write(f"**Complexity:** {current_task['complexity']}")
    st.write(current_task["prompt"])
    st.error("⚡ Warning: Large Language Model queries consume significant energy. Please aim for concise and efficient requests. The best prctise would be to use a standard search engine because it uses up to 10 times less energy than a LLM!")
    
    response = st.text_area("Your response", key=f"response_{st.session_state.task_index}")
    disabled = not response.strip()
    
    col1, col2 = st.columns(2)
    
    with col1:
        submitted = st.button("Submit", disabled=disabled, key=f"submit_{st.session_state.task_index}", type="primary", use_container_width=True)
    
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
        save_response_data(current_task, response, used_alternative_search=False)
        
        
        st.success("Response submitted!")
        time.sleep(1)
        
        if st.session_state.task_index < len(st.session_state.tasks) - 1:
            st.session_state.task_index += 1
            st.session_state.show_transition = True
            st.rerun()
        else:
            st.session_state.study_completed = True
            st.rerun()