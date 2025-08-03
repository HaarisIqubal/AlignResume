# import requests
# from bs4 import BeautifulSoup
# from typing import Optional, List
# from pydantic import BaseModel, ValidationError
# import json
# from langchain_core.prompts import PromptTemplate
# from langchain.llms.ollama import Ollama
# from langchain_core.output_parsers import JsonOutputParser
# from model

# def fetch_job_posting_text(url: str) -> str:
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     return soup.get_text(separator="\n")

# def build_langchain_chain():
#     parser = JsonOutputParser(pydantic_object=JobPosting)
#     prompt = PromptTemplate(
#         template="""
# You are an information extraction engine. Extract the job posting data according to the following schema:

# {format_instructions}

# Job Posting:
# {job_text}
# """,
#         input_variables=["job_text"],
#         partial_variables={"format_instructions": parser.get_format_instructions()}
#     )
#     llm = Ollama(model="gemma3:latest")
#     chain = prompt | llm | parser
#     return chain

# def process_job_posting(url: str):
#     print("Fetching job posting text...")
#     job_text = fetch_job_posting_text(url)

#     print("Running through LangChain...")
#     chain = build_langchain_chain()
#     job_posting = chain.invoke({"job_text": job_text})

#     # print("\n✅ Structured Job Posting:")
#     # print(job_posting.json(indent=2))

# if __name__ == "__main__":
#     job_url = input("Enter job posting URL: ").strip()
#     process_job_posting(job_url)





import json
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from langchain.schema.output_parser import StrOutputParser
from ..model.JobPostingSchema import JobPosting

def extract_job_posting_detail(raw_data: str) -> JobPosting:
    """Extract structured resume information using LLM"""
    prompt = PromptTemplate(
            template="""
    You are an information extraction engine. Extract the job posting data according to the following schema:
    {format_instructions}
    Job Posting:
    {job_text}
    """,
            input_variables=["job_text","format_instructions"]
        )

    parser = PydanticOutputParser(pydantic_object=JobPosting)
    chain = _init_ollama_llm(prompt=prompt)

    try:
        raw_output = chain.invoke({"job_text": raw_data,
                                    "format_instructions": parser.get_format_instructions()})
        raw_output = _cleanup_llm_output(raw_output)
        parsed_json = json.loads(raw_output)
        resume_model = JobPosting(**parsed_json)
        return resume_model
    except Exception as e:
        print(f"Exception {e}")
        return JobPosting(
        job_title=None,
        department=None,
        job_type=None,
        start_date=None,
        location=None,
        remote_option=None,
        travel_requirement=None,

        education_level=None,
        education_fields=[],
        certifications_required=[],

        experience_years=None,
        experience_domains=[],
        project_examples=[],

        hard_skills=[],
        soft_skills=[],
        tools_platforms=[],
        languages_required=[],

        responsibilities=[],
        performance_indicators=[],
        personal_traits=[],

        legal_eligibility=None,
        work_authorization=None,
        relocation_support=None,

        employer_name=None,
        employer_type=None,
        company_culture=[],
        mission_focus=[],
        diversity_inclusion=None,

        application_mode=None,
        application_requirements=[],
        interview_stages=None,
        selection_criteria=[],

        salary_range=None,
        posting_date=None,
        application_deadline=None,
        job_reference_id=None,

        reporting_to=None,
        team_size=None,
        cross_functional=None,
        internal_collaboration=[],
        external_stakeholders=[],

        strategic_goals=[],
        transformation_initiatives=[],
        success_metrics=[],
        leadership_expectations=None,
        decision_making_scope=None,
        learning_opportunities=[],
        career_path=None
    )
    finally:
        print("Finally passed")


def _init_ollama_llm(prompt: PromptTemplate) -> Runnable:
    """Initialize Ollama LLM with prompt chain"""
    language_model = ChatOllama(model="gemma3n:latest", temperature=0)
    chain:Runnable = prompt | language_model | StrOutputParser()
    return chain

def _cleanup_llm_output(raw_output: str) -> str:
    """Clean up LLM output to extract pure JSON"""
    if raw_output.startswith("```json"):
        raw_output = raw_output[len("```json"):].lstrip()
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3].rstrip()
    return raw_output.strip()