import streamlit as st


def render_example():
    st.title("Task Tutorial")
    

    st.markdown("""
    You must request answers from a chatbot based on a given task. Alternatively use another search method such as a simple Google search if you prefer.
    **Please read the given tasks carefully.**
    """)

    st.write("---")

    st.subheader("How to perform the task")
    st.markdown("### Step 1.")
    st.markdown("First you are given a task to perform. Here you should read carefully and filter out the most important information. An example for such a task would be:")

    # 1. Task Description
    with st.container(border=True):
        st.markdown("""
        You are advising a small developing country that wants to reduce carbon emissions while maintaining rapid industrial growth. The country has limited administrative capacity, strong political resistance from manufacturers, and concerns about economic competitiveness. You need to evaluate whether a carbon tax or a cap-and-trade system would be more effective and realistic under these constraints.\n\n**Task:** Use the text field below to explain your context and ask the chatbot to compare the two approaches and make a recommendation, or switch to a web browser to do a simple Google search."</p>
        
        """, unsafe_allow_html=True)

    # 2. User's Prompt
    st.markdown(" ### Step 2.")
    st.markdown(" Now you are given two options:")
    st.markdown(" - **Option 1:** Use an alternative search by clicking directly on the alternative search button to simple retrieve the needed information.")
    st.button("Alternative Search", help="Use a different search method like a simple Google Search", use_container_width=True)


    st.markdown(""" - **Option 2:** Use the text area below to provide a detailed prompt to the chatbot. For example, you might write:""")
    with st.container(border=True):
        st.markdown("""

                    I need help evaluating climate policy options for a small developing country with specific constraints.

                    The country wants to reduce carbon emissions while maintaining rapid industrial growth, but faces:
                    - Limited administrative capacity
                    - Strong political resistance from manufacturers
                    - Concerns about economic competitiveness

                    Please compare **carbon tax** versus **cap-and-trade systems** for this context. 

                    For each approach, analyze:

                    1. Implementation complexity and administrative requirements
                    2. Political feasibility given manufacturer resistance
                    3. Impact on economic competitiveness
                    4. Effectiveness at reducing emissions under these constraints
                    5. Potential hybrid or modified approaches that might work better

                    Finally, provide a clear recommendation on which policy (or combination) would be most effective and realistic for this country, with specific reasoning based on the constraints mentioned.
                    """)
        
    # 3. Submission Instructions
    st.markdown(" ### Step 3.")
    st.markdown("After providing your prompt, you have to either press **command/ctrl and Enter** or click on a random spot outside the text area.")

    st.markdown(" ### Step 4.") 
    st.markdown(" Then you are able to submit your response by clicking the **submit** button.")
    st.button("Submit", type="primary", use_container_width=True)


    st.markdown(" Alternatively, if you changed your decision, you can click on the 'Alternative Search' button to use a different search method like a simple Google search.")

    st.write("---")

    st.write("")
    st.write("")
    
    if st.button("I understand the rules & task - Start Experiment", type="primary"):
        st.session_state.example_complete = True
        st.rerun()
                            
