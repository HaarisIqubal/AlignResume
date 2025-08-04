import streamlit as st
import tempfile
from ..tool.document_extractor import extract_pdf_document
from ..tool.job_crawler import crawl_job_detail
from .text_state_manager import text_manager
from ..tool.resume_extractor import extract_resume_detail
from ..tool.job_extractor import extract_job_posting_detail
from ..tool.resume_generator import generate_output_resume

def sidebar_view():
    with st.sidebar:
        st.subheader("Automate CV Building 🦾")
        docs_file = st.file_uploader("Upload your CV", type=['pdf'])
        original_pdf_path = ""
        if st.button('Process CV'):
            with st.spinner("Processing...."):
                if docs_file.type == "application/pdf":
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(docs_file.read())
                            tmp_file_path = tmp_file.name
                            original_pdf_path = tmp_file_path
                    markdown_content = extract_pdf_document(tmp_file_path)
                    text_manager.set_text('resume_text', markdown_content)
                    resume_structure = extract_resume_detail(markdown_content)
                    text_manager.set_text('resume_extraction', resume_structure.model_dump_json(indent=2))
                    
                    

        job_link = st.text_input("Enter Job portal URL", type="default")

        if st.button("Extract job description"):
            if len(job_link) > 0:
                crawl_job = crawl_job_detail(job_link)
                text_manager.set_text("job_description", crawl_job)
                extracted_job_posting = extract_job_posting_detail(crawl_job)
                text_manager.set_text("job_extraction", extracted_job_posting.model_dump_json(indent=2))
            else:
                st.warning("Enter Job url to fetch the data.")



        user_message = st.text_area("Enter your CV description.")

        if st.button("Let's build it 🔨..."):
            if len(user_message) > 0:
                markdown_text = text_manager.get_text("resume_text")
                with st.spinner("⏳ Generating tailored resume..."):
                    try:
                        # Generate resume with original PDF path (can be None)
                        result = generate_output_resume(
                            user_message=user_message, 
                            pdf_raw=markdown_text,
                            original_pdf_path=original_pdf_path
                        )
                        text_manager.set_resume_result(result)
                        st.success("✅ CV processed successfully!")
                    except Exception as e:
                        print(f"Exception {e}")
