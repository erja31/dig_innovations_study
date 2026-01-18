import streamlit as st
import time
from src.storage import save_response_data

def analyze_prompt_energy(prompt):
    """
    Analyze the prompt and estimate relative energy consumption.
    Returns a dictionary with energy score and feedback messages.
    """

    if not prompt.strip():
        return {
            "score": 0,
            "level": "none",
            "messages": [],
        }
    
    # High-energy keywords that indicate complex operations
    high_energy_keywords = [
        "analyze", "analyse", "comprehensive", "create", "detailed", "elaborate", "explain", "explain in depth",
        "compare", "summarize", "translate", "write a long", "generate multiple",
        "create a list of", "provide examples", "step by step", "thorough", "develop", "design",
        "extensive", "in-depth", "complete analysis", "full report", "step-by-step", "recommend", "measure", "report", "list",
    ]
    
    # Medium-energy keywords
    medium_energy_keywords = [
        "describe", "explain", "tell me about", "what is", "how does", "provide",
        "give me", "show me", "help me understand", "outline", "write", "classify", "identify", "generate", "justify", "translate"
    ]
    
    # Calculate energy factors
    word_count = len(prompt.split())
    
    # Count high and medium energy keywords
    prompt_lower = prompt.lower()
    high_energy_count = sum(1 for keyword in high_energy_keywords if keyword in prompt_lower)
    medium_energy_count = sum(1 for keyword in medium_energy_keywords if keyword in prompt_lower)
    
    # Calculate energy score (0-100)
    energy_score = 0
    messages = []
    
    # Length-based scoring
    if word_count > 70:
        energy_score += 30
        messages.append(f"⚠️ Your prompt is quite long ({word_count} words). Consider being more concise.")
    elif word_count > 30:
        energy_score += 15
        messages.append(f"Your prompt is moderately long ({word_count} words).")
    
    # Keyword-based scoring
    if high_energy_count > 0:
        energy_score += high_energy_count * 20
        keywords_found = [kw for kw in high_energy_keywords if kw in prompt_lower]
        messages.append(f"High-energy keywords detected: {', '.join(keywords_found[:3])}. These require more computational resources.")
    
    if medium_energy_count > 0:
        energy_score += medium_energy_count * 10
    
    # Check for multiple requests
    if prompt.count("and") > 3 or prompt.count(",") > 5:
        energy_score += 15
        messages.append("Your prompt contains multiple requests. Consider breaking them into separate queries.")
    
    # Determine energy level
    if energy_score >= 70:
        level = "high"
        messages.insert(0, "🔴 HIGH ENERGY CONSUMPTION EXPECTED")
    elif energy_score >= 40:
        level = "medium"
        messages.insert(0, "🟡 MODERATE ENERGY CONSUMPTION")
    elif energy_score > 0:
        level = "low"
        messages.insert(0, "🟢 LOW ENERGY CONSUMPTION")
    else:
        level = "minimal"
        messages.insert(0, "✅ MINIMAL ENERGY CONSUMPTION")
    
    return {
        "score": min(energy_score, 100),
        "level": level,
        "messages": messages,
    }


def render_feedback_nudge():
    st.title("Chat Interface")
    current_task = st.session_state.tasks[st.session_state.task_index]

    # Calculate human-readable progress
    current_number = st.session_state.task_index
    total_tasks = len(st.session_state.tasks)

    # Display the progress as the header
    st.markdown(f"### Task {current_number} of {total_tasks}")
    st.write(current_task["prompt"])
    
    # Initialize tracking variables for this task if not already present
    task_key = f"task_{st.session_state.task_index}"
    if f"{task_key}_previous_response" not in st.session_state:
        st.session_state[f"{task_key}_previous_response"] = ""
        st.session_state[f"{task_key}_version_count" ] = 0
    
    st.caption("⚡ This interface provides real-time feedback on the energy consumption of your prompt. Click outside of the text field or press 'command/ctrl + enter' to update the feedback.")
    
    response = st.text_area(
        "Your response",
        key=f"response_{st.session_state.task_index}",
        help="Type your prompt here. You'll receive real-time feedback on its energy consumption.",
        on_change=None  # This triggers rerun on every change
    )

    # Create a container for real-time feedback that appears above the text area
    feedback_container = st.container()
    
    # Show real-time feedback in the container
    with feedback_container:
        if response.strip():
            analysis = analyze_prompt_energy(response)
            
            # Track changes: save each version when response changes
            previous_response = st.session_state[f"{task_key}_previous_response"]
            if response != previous_response and response.strip():
                # Increment version count
                st.session_state[f"{task_key}_version_count"] += 1
                version = st.session_state[f"{task_key}_version_count"]
                
                # Create the task identifier with version suffix
                task_identifier = f"{st.session_state.task_index}_{version}"
                
                # Save this version
                save_response_data(task_identifier, current_task, response, used_alternative_search=False)
                
                # Update the previous response
                st.session_state[f"{task_key}_previous_response"] = response
            
            # Create columns for metric display at the top
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Word Count", len(response.split()))
            with col2:
                st.metric("Energy Score", f"{analysis['score']}/100")
            with col3:
                # Color-code the level
                level_emoji = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢",
                    "minimal": "✅"
                }
                st.metric("Level", f"{level_emoji.get(analysis['level'], '⚪')} {analysis['level'].upper()}")
            
            st.markdown("---")
            
            # Show detailed feedback based on energy level
            if analysis["level"] == "high":
                for message in analysis["messages"]:
                    st.markdown(f"• {message}")
                
            elif analysis["level"] == "medium":
                for message in analysis["messages"]:
                    st.markdown(f"• {message}")
                
            elif analysis["level"] == "low":
                for message in analysis["messages"]:
                    st.markdown(f"• {message}")
            else:
                st.success("Your prompt is energy-efficient!")
            
            # Show tips if score is high
            if analysis["score"] > 40:
                with st.expander("💡 Tips to reduce energy consumption", expanded=analysis["score"] > 30):
                    st.markdown("""
                    - **Be specific and concise**: Avoid asking for "comprehensive" or "detailed" explanations unless necessary
                    - **One task at a time**: Break complex requests into simpler, separate queries
                    - **Avoid redundancy**: Don't ask for the same information in multiple ways
                    - **Use precise language**: Clear, direct questions are more efficient
                    - **Avoid specific keywords that could lead to longer responses**: Words like "analyze", "detailed", "comprehensive", or "in-depth" can increase response length
                    - **Limit scope**: Request only the information you actually need
                    """)
    
    disabled = not response.strip()
    
    col1, col2 = st.columns(2)
    
    with col1:
        submitted = st.button("Submit", disabled=disabled, key=f"submit_{st.session_state.task_index}", type="primary", use_container_width=True)
    
    with col2:
        alt_search = st.button(
            "Alternative Search",
            key=f"alt_search_{st.session_state.task_index}",
            help="Use a different search method like a simple Google Search",
            use_container_width=True
        )
    
    if alt_search:
        # Move to next task
        save_response_data(f"{st.session_state.task_index}_alt", current_task, response, used_alternative_search=True)
        
        if st.session_state.task_index < len(st.session_state.tasks) - 1:
            st.session_state.task_index += 1
            st.session_state.show_transition = True
            st.rerun()
        else:
            st.session_state.study_completed = True
            st.rerun()

    elif submitted and response.strip():
        analysis = analyze_prompt_energy(response)
        
        st.success("Response submitted!")
        
        time.sleep(1)
        
        if st.session_state.task_index < len(st.session_state.tasks) - 1:
            st.session_state.task_index += 1
            st.session_state.show_transition = True
            st.rerun()
        else:
            st.session_state.study_completed = True
            st.rerun()