# '''
# | Goal                | Best Fields to Embed Eg.                         |
# | ------------------- | ---------------------------------------------- |
# | **CV–job matching** | skills, experience, responsibilities, values   |
# | **Job clustering**  | department, mission, strategic goals           |
# | **Search/filter**   | include more general text, less personal match |

# '''

# from ..model.JobPostingSchema import JobPosting


# job_posting = { "job_title": "Scrum Master", "department": null, "job_type": "Full-Time", "start_date": null, "location": "Romania", "remote_option": null, "travel_requirement": null, "education_level": "Bachelor's degree", "education_fields": [ "Computer Science", "Information Technology", "Business", "Related Field" ], "certifications_required": [ "Scrum Master" ], "experience_years": "3+", "experience_domains": [ "Scrum Master", "Agile Coach" ], "project_examples": [], "hard_skills": [ "Jira", "Confluence", "Project Management Software" ], "soft_skills": [ "Communication Skills", "Problem-solving", "Conflict Resolution", "Emotional Intelligence", "Self-motivation", "Teamwork", "Multitasking", "Organizational Skills", "Time Management", "Verbal Communication", "Written Communication" ], "tools_platforms": [ "Jira", "Confluence" ], "languages_required": [ "English" ], "responsibilities": [ "Establishing agile principles and methods", "Building a supportive agile work model", "Moderating retrospectives and workshops", "Supporting the team leader and development team", "Promoting continuous improvement", "Ensuring adherence to agile frameworks", "Assisting in removing obstacles", "Encouraging self-organization", "Conducting training and coaching", "Supporting sprint planning and execution", "Ensuring transparent communication", "Promoting collaboration and knowledge sharing" ], "performance_indicators": [], "personal_traits": [ "Experienced", "Professional" ], "legal_eligibility": null, "work_authorization": null, "relocation_support": null, "employer_name": "Schaeffler Romania S.R.L.", "employer_type": "Technology Company", "company_culture": [], "mission_focus": [], "diversity_inclusion": null, "application_mode": null, "application_requirements": [], "interview_stages": null, "selection_criteria": [], "salary_range": null, "posting_date": null, "application_deadline": null, "job_reference_id": null, "reporting_to": null, "team_size": null, "cross_functional": null, "internal_collaboration": [], "external_stakeholders": [], "strategic_goals": [], "transformation_initiatives": [], "success_metrics": [], "leadership_expectations": null, "decision_making_scope": null, "learning_opportunities": [], "career_path": null }






# embedding_field_config = {
#     # 🔹 Role & Responsibility
#     "job_title": True,
#     "department": True,
#     "job_type": True,
#     "responsibilities": True,
#     "reporting_to": True,
#     "team_size": True,

#     # 🔹 Skills & Experience
#     "education_level": True,
#     "education_fields": True,
#     "experience_years":True,
#     "experience_domains": True,
#     "project_examples": True,
#     "hard_skills": True,
#     "soft_skills": True,
#     "tools_platforms": True,
#     "languages_required":True,

#     # 🔹 Strategic & Performance Focus
#     "strategic_goals": True,
#     "performance_indicators": True,
#     "success_metrics": True,
#     "leadership_expectations": True,
#     "transformation_initiatives":True,
#     "success_metrics":True,
    

#     # 🔹 Company Fit & Values
#     "mission_focus": True,
#     "company_culture": True,
#     "diversity_inclusion": True,

#     # 🔹 Location & Legal Context
#     "location": True,
#     "remote_option": True,
#     "travel_requirement": True,
#     "legal_eligibility": True,
#     "work_authorization": True,
#     "relocation_support": True,
#     "employer_name":True,

#     # 🚫 Metadata (usually not embedded)
#     "start_date": False,
#     "posting_date": False,
#     "application_deadline": False,
#     "job_reference_id": False,
#     "application_mode": False,
#     "salary_range": False,
#     "application_requirements":False,
#     "interview_stages":False,
#     "selection_criteria":False,
#     "cross_functional":False,
#     "internal_collaboration":False,
#     "external_stakeholders":False,
#     "decision_making_scope":False,
#     "leadership_expectations":False,
#     "learning_opportunities":False,
#     "career_path":False
# }


# def get_embedding_text(job_posting: JobPosting, config: dict) -> str:
#     text_chunks = []
#     for field, use in config.items():
#         if not use:
#             continue
#         value = getattr(job_posting, field, None)
#         if isinstance(value, list):
#             text_chunks.append(" ".join(value))
#         elif isinstance(value, str):
#             text_chunks.append(value)
#     return " ".join(text_chunks)



# job_posting_obj = JobPosting(**job_posting)

# embedding_text = get_embedding_text(job_posting_obj, embedding_field_config)

# print(embedding_text)