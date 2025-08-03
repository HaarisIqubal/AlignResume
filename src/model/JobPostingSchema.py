from pydantic import BaseModel, ValidationError
from typing import Optional, List

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
