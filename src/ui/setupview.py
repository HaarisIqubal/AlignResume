import streamlit as st
from .sidebar import sidebar_view
from .text_state_manager import text_manager

def setup_view():
    st.set_page_config(page_title='CV Maker', page_icon='📑', layout='centered')
    st.title('Automize the process of CV making  📑')
    st.write("This app helps you to make the process of CV making a breeze.")
    
    # Initialize multiple text states using a dictionary
    if 'text_states' not in st.session_state:
        st.session_state.text_states = {
            'extracted_resume': "",
            'job_description': ""
        }
    
    
    sidebar_view()

    resume_text = text_manager.get_text("resume_text")
    job_description = text_manager.get_text("job_description")
    st.header("Resume Data")
    if len(resume_text) > 0:
        st.success("Resume Extracted ✅")
        with st.expander("View Resume Content"):
            st.text(resume_text)
    else:
        st.info("No resume uploaded yet.")

    st.header("Job Description")
    if len(job_description) > 0:
        st.success("Job Description is extracted ✅")
        with st.expander("View job extracted Content"):
            st.markdown(job_description)
    else:
        st.info("No job description extracted yet")


    st.header("Comparison and Gap Table")

    st.header("Generated CV")