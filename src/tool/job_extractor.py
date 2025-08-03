import json
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from ..model.JobPostingSchema import JobPosting
from .llm_manager import llm_manager

def extract_job_posting_detail(raw_data: str) -> JobPosting:
    """
    Extract structured job information using LLM.
    Parameters
    ----------
    raw_data : str
        The string of raw extracted data from the job posting website.

    Returns
    -------
    job_posting_model : JobPosting
            This will return the value of job_posting in formatted way of pydantic.
    """
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
    chain = llm_manager.init_llm_chain(prompt=prompt)

    try:
        raw_output = chain.invoke({"job_text": raw_data,
                                    "format_instructions": parser.get_format_instructions()})
        raw_output = llm_manager.cleanup_llm_output(raw_output)
        parsed_json = json.loads(raw_output)
        job_posting_model = JobPosting(**parsed_json)
        return job_posting_model
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