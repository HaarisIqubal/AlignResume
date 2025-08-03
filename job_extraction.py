import requests
from bs4 import BeautifulSoup
from typing import Optional, List
from pydantic import BaseModel, ValidationError
import json
from langchain_core.prompts import PromptTemplate
from langchain.llms.ollama import Ollama
from langchain_core.output_parsers import JsonOutputParser

# Define the extended JobPosting Pydantic model
class JobPosting(BaseModel):
    job_title: Optional[str]
    department: Optional[str]
    job_type: Optional[str]
    start_date: Optional[str]
    location: Optional[str]
    remote_option: Optional[str]
    travel_requirement: Optional[str]

    education_level: Optional[str]
    education_fields: List[str] = []
    certifications_required: List[str] = []

    experience_years: Optional[str]
    experience_domains: List[str] = []
    project_examples: List[str] = []

    hard_skills: List[str] = []
    soft_skills: List[str] = []
    tools_platforms: List[str] = []
    languages_required: List[str] = []

    responsibilities: List[str] = []
    performance_indicators: List[str] = []
    personal_traits: List[str] = []

    legal_eligibility: Optional[str]
    work_authorization: Optional[str]
    relocation_support: Optional[str]

    employer_name: Optional[str]
    employer_type: Optional[str]
    company_culture: List[str] = []
    mission_focus: List[str] = []
    diversity_inclusion: Optional[str]

    application_mode: Optional[str]
    application_requirements: List[str] = []
    interview_stages: Optional[str]
    selection_criteria: List[str] = []

    salary_range: Optional[str]
    posting_date: Optional[str]
    application_deadline: Optional[str]
    job_reference_id: Optional[str]

    reporting_to: Optional[str]
    team_size: Optional[str]
    cross_functional: Optional[bool]
    internal_collaboration: List[str] = []
    external_stakeholders: List[str] = []

    strategic_goals: List[str] = []
    transformation_initiatives: List[str] = []
    success_metrics: List[str] = []
    leadership_expectations: Optional[str]
    decision_making_scope: Optional[str]
    learning_opportunities: List[str] = []
    career_path: Optional[str]


def fetch_job_posting_text(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator="\n")

def build_langchain_chain():
    parser = JsonOutputParser(pydantic_object=JobPosting)
    prompt = PromptTemplate(
        template="""
You are an information extraction engine. Extract the job posting data according to the following schema:

{format_instructions}

Job Posting:
{job_text}
""",
        input_variables=["job_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    llm = Ollama(model="gemma3:latest")
    chain = prompt | llm | parser
    return chain

def process_job_posting(url: str):
    print("Fetching job posting text...")
    job_text = fetch_job_posting_text(url)

    print("Running through LangChain...")
    chain = build_langchain_chain()
    job_posting = chain.invoke({"job_text": job_text})

    print("\n✅ Structured Job Posting:")
    print(job_posting.json(indent=2))

if __name__ == "__main__":
    job_url = input("Enter job posting URL: ").strip()
    process_job_posting(job_url)
