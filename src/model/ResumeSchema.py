from pydantic import BaseModel, Field
from typing import List,Optional

class Experience(BaseModel):
    title: Optional[str] = None 
    company: Optional[str] = None 
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    experience_domain: List[str] = Field( default_factory=list, description="this should be list of domains of the description")
    keywords: List[str] = Field( default_factory=list, description="A list of 1 keyword each from all the experiences from the past")
    previous_job_titles: List[str] = Field( default_factory=list, description="A list of all the job titles from the past")


class Total_Experience(BaseModel):
    experience_years: Optional[str] = None
    experience_domains: List[str] = Field(default_factory=list)
    project_examples: List[str] = Field(default_factory=list)
    certifications: List[str] = Field( default_factory=list, description='Any certification done is listed here as a List of certificates if not from a solid vendor, it can be left.')

class Education(BaseModel):
    degree: Optional[str] = None 
    institution: Optional[str] = None 
    start_data: Optional[str] = Field(default_factory=list)
    end_data: Optional[str] = Field(default_factory=list)
    education_field:Optional[str] = Field(default_factory=list)

class Responsibilities(BaseModel):
    responsibilities: List[str] = Field(default_factory=list)
    personal_traits: List[str] = Field(default_factory=list)
    transformation_initiatives: List[str] = Field(default_factory=list)
    leadership_expectations: Optional[str] = Field(default_factory=list)
    decision_making_scope: Optional[str] = Field(default_factory=list)

class Skills(BaseModel):
    hard_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    tools_platforms: List[str] = Field(default_factory=list)
    languages_required: List[str] = Field(default_factory=list)
class Personal(BaseModel):
    name: Optional[str] = None 
    email: Optional[str] = Field(default_factory=list)
    phone: Optional[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    total_experience: Optional[Total_Experience] = Field(default_factory=list)
    skills: Optional[Skills] = Field(default_factory=list)
    responsibilities: Optional[Responsibilities] = Field(default_factory=list)
