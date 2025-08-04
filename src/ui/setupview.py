import os
import streamlit as st
from .sidebar import sidebar_view
from .text_state_manager import text_manager
from ..tool.llm_manager import llm_manager

def setup_view():
    st.set_page_config(page_title='CV Maker', page_icon='📑', layout='centered')
    st.title('Automize the process of CV making  📑')
    st.write("This app helps you to make the process of CV making a breeze.")

    st.subheader("🤖 LLM Configuration")

    #Provider selection
    provider = st.selectbox(
        "Select LLM Provider",
        options=list(llm_manager.providers.keys()),
        key="llm_provider"
    )
    
    # Model selection based on provider
    available_models = llm_manager.get_available_models(provider)
    model = st.selectbox(
        "Select Model",
        options=available_models,
        key="llm_model"
    )

    
    # Store LLM config in session state
    st.session_state.llm_config = {
        "provider": provider,
        "model": model    
        }
    # Show current configuration
    with st.expander("Current LLM Config"):
        st.write(f"**Provider:** {provider}")
        st.write(f"**Model:** {model}")
    
    st.divider()

    # Initialize multiple text states using a dictionary
    if 'text_states' not in st.session_state:
        st.session_state.text_states = {
            'resume_text': '',
            'resume_extraction':'',
            'job_description': '',
            'job_extraction': ''
        }
    
    
    sidebar_view()

    resume_text = text_manager.get_text("resume_text")
    resume_extraction = text_manager.get_text("resume_extraction")
    job_extraction = text_manager.get_text('job_extraction')
    job_description = text_manager.get_text("job_description")
    st.subheader("Resume Data")
    if len(resume_text) > 0:
        st.success("Resume Text ✅")
        with st.expander("View Resume Content"):
            st.text(resume_text)
    else:
        st.info("No resume uploaded yet.")

    if len(resume_extraction) > 0:
        st.success("Resume extraction")
        with st.expander("View resume structure"):
            st.text(resume_extraction)
    else:
        st.info("No resume uploaded yet.")

    st.subheader("Job Description")
    if len(job_description) > 0:
        st.success("Job description is extracted ✅")
        with st.expander("View job extracted Content"):
            st.markdown(job_description)
    else:
        st.info("No job description extracted yet")

    if len(job_extraction) > 0:
        st.success("Job extraction is done ✅")
        with st.expander("View job extracted structure"):
            st.markdown(job_extraction)
    else:
        st.info("No job description extracted yet")
    
    st.subheader("Comparison and Gap Table")

    st.subheader("Generated CV")
    # Download button

    result = text_manager.get_resume_result()
    if result.get('edited_pdf_path') and os.path.exists(result['edited_pdf_path']):
        with open(result['edited_pdf_path'], "rb") as pdf_file:
            st.download_button(
                label="📥 Download Tailored Resume",
                data=pdf_file.read(),
                file_name="tailored_resume.pdf",
                mime="application/pdf",
                key="download_tailored_resume"
            )

def _validate_llm_config() -> bool:
    """Validate LLM configuration"""
    config = st.session_state.get('llm_config', {})
    
    if not config.get('provider') or not config.get('model'):
        return False
    
    provider = config.get('provider')
    if llm_manager.requires_api_key(provider) and not config.get('api_key'):
        return False
    
    return True