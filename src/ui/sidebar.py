import streamlit as st
import tempfile
from ..tool.document_extractor import extract_pdf_document
from ..tool.job_extractor import extract_job_detail
from .text_state_manager import text_manager
from ..tool.resume_extractor import extract_resume_detail

def sidebar_view():
    with st.sidebar:
        st.subheader("Automate CV Building")
        docs_file = st.file_uploader("Upload your CV", type=['pdf'])

        if st.button('Process CV'):
            with st.spinner("Processing...."):
                if docs_file.type == "application/pdf":
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(docs_file.read())
                            tmp_file_path = tmp_file.name
                    markdown_content = extract_pdf_document(tmp_file_path)
                    text_manager.set_text('resume_text', markdown_content)
                    resume_structure = extract_resume_detail(markdown_content)
                    text_manager.set_text('resume_extraction', resume_structure.model_dump_json(indent=2))
                    
                    

        job_link = st.text_input("Enter Job portal URL", type="default")

        if st.button("Extract job description"):
            if len(job_link) > 0:
                extracted_job = extract_job_detail(job_link)
                text_manager.set_text("job_description", extracted_job)


        cv_description = st.text_area("Enter your CV description.")

        st.button("Let's build it 🔨...")