from pydantic import BaseModel
from typing import List,Optional

class Experience(BaseModel):
    title: str
    company: str
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]

class Education(BaseModel):
    degree: str
    institution: str
    start_data: Optional[str]
    end_data: Optional[str]

class Personal(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    education: List[Education]
    experience: List[Experience]
