# from pydantic import BaseModel
# from typing import Optional, List

# class JobPosting(BaseModel):
#     #Job basics
#     job_title: Optional[str] = None
#     department: Optional[str] = None
#     job_type: Optional[str] = None
#     start_date: Optional[str] = None
#     location: Optional[str] = None
#     remote_option: Optional[str] = None
#     travel_requirement: Optional[str] = None
#     reporting_to: Optional[str] = None
#     job_reference_id: Optional[str] = None

#     #Education
#     education_level: Optional[str] = None
#     education_fields: List[str] = []
#     certifications_required: List[str] = []

#     #Experience
#     experience_years: Optional[str] = None
#     experience_domains: List[str] = []
#     project_examples: List[str] = []

#     #Skills
#     hard_skills: List[str] = []
#     soft_skills: List[str] = []
#     tools_platforms: List[str] = []
#     languages_required: List[str] = []

#     #Roles and responsibilities
#     responsibilities: List[str] = []
#     performance_indicators: List[str] = []
#     personal_traits: List[str] = []
#     strategic_goals: List[str] = []
#     transformation_initiatives: List[str] = []
#     success_metrics: List[str] = []
#     leadership_expectations: Optional[str] = None
#     decision_making_scope: Optional[str] = None


#     # Legal & Eligibility
#     legal_eligibility: Optional[str] = None
#     work_authorization: Optional[str] = None
#     relocation_support: Optional[str] = None

#     # Company and Culture
#     employer_name: Optional[str] = None
#     employer_type: Optional[str] = None
#     company_culture: List[str] = []
#     mission_focus: List[str] = []
#     diversity_inclusion: Optional[str] = None

#     #Application Process
#     application_mode: Optional[str] = None
#     application_requirements: List[str] = []
#     interview_stages: Optional[str] = None
#     selection_criteria: List[str] = []

#     # Compensation & Timeline
#     salary_range: Optional[str] = None
#     posting_date: Optional[str] = None
#     application_deadline: Optional[str] = None
    
#     # Team & Collaboration
#     team_size: Optional[str] = None
#     cross_functional: Optional[bool] = None
#     internal_collaboration: List[str] = []
#     external_stakeholders: List[str] = []

#     # Growth & Career Development
#     learning_opportunities: List[str] = []
#     career_path: Optional[str] = None




from pydantic import BaseModel
from typing import Optional, List


class Job_Basics(BaseModel):
    #Job basics
    job_title: Optional[str] = None
    department: Optional[str] = None
    job_type: Optional[str] = None
    start_date: Optional[str] = None
    location: Optional[str] = None
    remote_option: Optional[str] = None
    travel_requirement: Optional[str] = None
    reporting_to: Optional[str] = None
    job_reference_id: Optional[str] = None

class Education(BaseModel):
    #Education
    education_level: Optional[str] = None
    education_fields: List[str] = []
    certifications_required: List[str] = []

class Experience(BaseModel):
    #Experience
    experience_years: Optional[str] = None
    experience_domains: List[str] = []
    project_examples: List[str] = []

class Skills(BaseModel):
    #Skills
    hard_skills: List[str] = []
    soft_skills: List[str] = []
    tools_platforms: List[str] = []
    languages_required: List[str] = []

class Role_Responsibility(BaseModel):
    #Roles and responsibilities
    responsibilities: List[str] = []
    performance_indicators: List[str] = []
    personal_traits: List[str] = []
    strategic_goals: List[str] = []
    transformation_initiatives: List[str] = []
    success_metrics: List[str] = []
    leadership_expectations: Optional[str] = None
    decision_making_scope: Optional[str] = None

class Legal_Eligibility(BaseModel):
    # Legal & Eligibility
    legal_eligibility: Optional[str] = None
    work_authorization: Optional[str] = None
    relocation_support: Optional[str] = None

class Company_Culture(BaseModel):
    # Company and Culture
    employer_name: Optional[str] = None
    employer_type: Optional[str] = None
    company_culture: List[str] = []
    mission_focus: List[str] = []
    diversity_inclusion: Optional[str] = None

class Application_Process(BaseModel):
    #Application Process
    application_mode: Optional[str] = None
    application_requirements: List[str] = []
    interview_stages: Optional[str] = None
    selection_criteria: List[str] = []

class Compensation_Timeline(BaseModel):
    # Compensation & Timeline
    salary_range: Optional[str] = None
    posting_date: Optional[str] = None
    application_deadline: Optional[str] = None

class Team_Collaboration(BaseModel):
    # Team & Collaboration
    team_size: Optional[str] = None
    cross_functional: Optional[bool] = None
    internal_collaboration: List[str] = []
    external_stakeholders: List[str] = []
class Growth_Career(BaseModel):
    # Growth & Career Development
    learning_opportunities: List[str] = []
    career_path: Optional[str] = None

class JobPosting(BaseModel):
    job_basics:Optional[Job_Basics]  =None
    education: Optional[Education] = None
    experience: Optional[Education] = None
    skills:Optional[Skills] = None    
    role_reponsibility: Optional[Role_Responsibility] = None
    legal_eligibility: Optional[Legal_Eligibility] = None
    company_culture: Optional[Company_Culture] = None
    application_process:Optional[Application_Process] = None
    compensation_timeline:Optional[Compensation_Timeline] = None
    team_collaboration: Optional[Team_Collaboration] = None
    growth_career:Optional[Growth_Career] = None
