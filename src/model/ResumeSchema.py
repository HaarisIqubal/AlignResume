from pydantic import BaseModel, Field
from typing import List,Optional

class Experience(BaseModel):
    title: str
    company: str
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    experience_domain: List[str] = Field( "this should be list of domains of the description above")

class Total_Experience(BaseModel):
    experience_years: Optional[str] = None
    experience_domains: List[str] = []
    project_examples: List[str] = []

class Education(BaseModel):
    degree: str
    institution: str
    start_data: Optional[str]
    end_data: Optional[str]
    education_field:Optional[str] = None

class Responsibilities(BaseModel):
    responsibilities: List[str] = []
    personal_traits: List[str] = []
    transformation_initiatives: List[str] = []
    leadership_expectations: Optional[str] = None
    decision_making_scope: Optional[str] = None

class Skills(BaseModel):
    hard_skills: List[str] = []
    soft_skills: List[str] = []
    tools_platforms: List[str] = []
    languages_required: List[str] = []
class Personal(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    education: List[Education]
    experience: List[Experience]
    total_experience: Optional[Total_Experience] = None
    skills: Optional[Skills] = None
    responsibilities: Optional[Responsibilities] = None
