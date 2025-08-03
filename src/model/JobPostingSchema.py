from pydantic import BaseModel
from typing import Optional, List

class JobPosting(BaseModel):
    job_title: Optional[str] = None
    department: Optional[str] = None
    job_type: Optional[str] = None
    start_date: Optional[str] = None
    location: Optional[str] = None
    remote_option: Optional[str] = None
    travel_requirement: Optional[str] = None

    education_level: Optional[str] = None
    education_fields: List[str] = []
    certifications_required: List[str] = []

    experience_years: Optional[str] = None
    experience_domains: List[str] = []
    project_examples: List[str] = []

    hard_skills: List[str] = []
    soft_skills: List[str] = []
    tools_platforms: List[str] = []
    languages_required: List[str] = []

    responsibilities: List[str] = []
    performance_indicators: List[str] = []
    personal_traits: List[str] = []

    legal_eligibility: Optional[str] = None
    work_authorization: Optional[str] = None
    relocation_support: Optional[str] = None

    employer_name: Optional[str] = None
    employer_type: Optional[str] = None
    company_culture: List[str] = []
    mission_focus: List[str] = []
    diversity_inclusion: Optional[str] = None

    application_mode: Optional[str] = None
    application_requirements: List[str] = []
    interview_stages: Optional[str] = None
    selection_criteria: List[str] = []

    salary_range: Optional[str] = None
    posting_date: Optional[str] = None
    application_deadline: Optional[str] = None
    job_reference_id: Optional[str] = None

    reporting_to: Optional[str] = None
    team_size: Optional[str] = None
    cross_functional: Optional[bool] = None
    internal_collaboration: List[str] = []
    external_stakeholders: List[str] = []

    strategic_goals: List[str] = []
    transformation_initiatives: List[str] = []
    success_metrics: List[str] = []
    leadership_expectations: Optional[str] = None
    decision_making_scope: Optional[str] = None
    learning_opportunities: List[str] = []
    career_path: Optional[str] = None
