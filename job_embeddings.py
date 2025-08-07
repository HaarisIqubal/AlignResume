'''
| Goal                | Best Fields to Embed Eg.                         |
| ------------------- | ---------------------------------------------- |
| **CV–job matching** | skills, experience, responsibilities, values   |
| **Job clustering**  | department, mission, strategic goals           |
| **Search/filter**   | include more general text, less personal match |

'''

from src.model.JobPostingSchema import JobPosting
from src.tool.embedding_util import get_similar_terms_from_llm, cleanup_llm_output, fetch_relevant_info, reconstruct_job_posting, extract_values_from_object, flatten_fields, embed_field_values
from sentence_transformers import SentenceTransformer
import json
import time 


# job_posting = { "job_title": "Scrum Master", "department": None, "job_type": "Full-Time", "start_date": None, "location": "Romania", "remote_option": None, "travel_requirement": None, "education_level": "Bachelor's degree", "education_fields": [ "Computer Science", "Information Technology", "Business", "Related Field" ], "certifications_required": [ "Scrum Master" ], "experience_years": "3+", "experience_domains": [ "Scrum Master", "Agile Coach" ], "project_examples": [], "hard_skills": [ "Jira", "Confluence", "Project Management Software" ], "soft_skills": [ "Communication Skills", "Problem-solving", "Conflict Resolution", "Emotional Intelligence", "Self-motivation", "Teamwork", "Multitasking", "Organizational Skills", "Time Management", "Verbal Communication", "Written Communication" ], "tools_platforms": [ "Jira", "Confluence" ], "languages_required": [ "English" ], "responsibilities": [ "Establishing agile principles and methods", "Building a supportive agile work model", "Moderating retrospectives and workshops", "Supporting the team leader and development team", "Promoting continuous improvement", "Ensuring adherence to agile frameworks", "Assisting in removing obstacles", "Encouraging self-organization", "Conducting training and coaching", "Supporting sprint planning and execution", "Ensuring transparent communication", "Promoting collaboration and knowledge sharing" ], "performance_indicators": [], "personal_traits": [ "Experienced", "Professional" ], "legal_eligibility": None, "work_authorization": None, "relocation_support": None, "employer_name": "Schaeffler Romania S.R.L.", "employer_type": "Technology Company", "company_culture": [], "mission_focus": [], "diversity_inclusion": None, "application_mode": None, "application_requirements": [], "interview_stages": None, "selection_criteria": [], "salary_range": None, "posting_date": None, "application_deadline": None, "job_reference_id": None, "reporting_to": None, "team_size": None, "cross_functional": None, "internal_collaboration": [], "external_stakeholders": [], "strategic_goals": [], "transformation_initiatives": [], "success_metrics": [], "leadership_expectations": None, "decision_making_scope": None, "learning_opportunities": [], "career_path": None }

job_posting = { 
    "job_basics": { "job_title": "Purchasing Framework, Digitalization & Risk Managment professional", "department": "Strategy & Business Development", "job_type": "Full-Time", "start_date": None, "location": "Thailand (implied by contact info)", "remote_option": None, "travel_requirement": None, "reporting_to": None, "job_reference_id": None }, "education": { "education_level": None, "education_fields": [], "certifications_required": [] }, "experience": { "education_level": "At least 3 years of experience", "education_fields": [ "Purchasing or equivalent", "network organization" ], "certifications_required": [] }, "skills": { "hard_skills": [ "Project management methods", "Data and Performance Management", "Risk Management (supply chain, delivery, financial, regulatory)", "Risk mitigation strategies", "Analytical skills", "Conceptual skills" ], "soft_skills": [ "Continuous Improvement", "Collaboration", "Capabilities improvement", "High proficiency in verbally and written Communicating skills on an international basis", "High ability and willingness to approach other persons and cultures in an unbiased and open manner", "Ability to work with diverse opinions and expectations", "Good interpersonal skills", "Curious", "Open minded", "Agility to engage people", "Good organizational and planning skills", "Independent working style", "Strategic thinking", "Takes the initiative", "Think out of the box", "Understand easily complex business matters", "Ability to deliver results under pressure", "Team player attitude", "Friendly", "Service oriented", "Independent and responsible way of working", "Quick comprehension", "Assertiveness" ], "tools_platforms": [], "languages_required": [ "English (written and spoken)" ] }, "role_reponsibility": { "responsibilities": [ "Continuous Improvement and improvement projects management", "Identify areas within the purchasing process that can be optimized for efficiency and cost-effectiveness", "Support to conduct regular reviews of purchasing activities to identify improvement opportunities", "Conducting necessary project management methods within the defined purchasing processes & systems by defining relevant objectives, collecting datas, excecution and contibuting to its long term success", "Support the Data and Performance Management team to define areas of improvement within the existing reporting and data management", "Support the management to assess the skills and capabilities of the purchasing team and identify areas for development", "Propose performance improvement plans, onboarding plans etc. with the collaboration with HR and QPP", "Ensure the accessibility and inortmation sharing of the trainings, tools and processes to the Purchasing teams in Asia Pacific", "Facilitate effective communication and collaboration between the purchasing team and other departments", "Participate in cross-functional projects and initiatives to drive overall business success", "Stay abreast of industry trends and emerging technologies that can enhance purchasing operations", "Foster a culture of innovation by encouraging team members to propose and implement new ideas", "Collaborate with Purchasing teams and other departments to support the integration of innovative solutions", "Identify potential risks in the supply chain, such delivery Risks, Financial risks etc. and regulatory changes", "Develop and implement risk mitigation strategies to minimize the impact of identified risks", "Monitor the external environment for emerging risks and adjust strategies accordingly" ], "performance_indicators": [], "personal_traits": [ "Curious", "Open minded", "Agility to engage people", "Independent working style", "Strategic thinking", "Takes the initiative", "Think out of the box", "Team player attitude", "Friendly", "Service oriented", "Independent and responsible way of working", "Assertiveness" ], "strategic_goals": [ "Drive overall business success", "Contribute to sustainable value creation for our stakeholders and society as a whole", "Advance how the world moves" ], "transformation_initiatives": [], "success_metrics": [], "leadership_expectations": "Information on leadership understanding is referred to schaeffler.com/leadership.", "decision_making_scope": None }, "legal_eligibility": { "legal_eligibility": None, "work_authorization": None, "relocation_support": None }, "company_culture": { "employer_name": "Schaeffler", "employer_type": "dynamic global technology company", "company_culture": [ "Entrepreneurial spirit", "Long history of private ownership", "Treat each other with respect", "Value all ideas and perspectives", "Appreciating our differences", "Inspire creativity and drive innovation" ], "mission_focus": [ "Partner to all of the major automobile manufacturers", "Partner to key players in the aerospace and industrial sectors", "Impact the future with innovation", "Advance how the world moves", "Sustainable value creation for our stakeholders and society as a whole" ], "diversity_inclusion": "As a global company with employees around the world, it is important to us that we treat each other with respect and value all ideas and perspectives. By appreciating our differences, we inspire creativity and drive innovation." }, "application_process": { "application_mode": None, "application_requirements": [], "interview_stages": None, "selection_criteria": [] }, "compensation_timeline": { "salary_range": None, "posting_date": None, "application_deadline": None }, "team_collaboration": { "team_size": None, "cross_functional": True, "internal_collaboration": [ "Facilitate effective communication and collaboration between the purchasing team and other departments", "Collaborate with Purchasing teams and other departments to support the integration of innovative solutions" ], "external_stakeholders": [] }, "growth_career": { "learning_opportunities": [ "Many development opportunities", "Assess the skills and capabilities of the purchasing team and identify areas for development", "Propose performance improvement plans, onboarding plans", "Ensure the accessibility and information sharing of the trainings, tools and processes" ], "career_path": "Exciting assignments and outstanding development opportunities await you" } }


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


embedding_field_config = {
    # 🔹 Role & Responsibility
    "job_basics.job_title": True,
    "job_basics.department": True,
    "job_basics.job_type": True,
    "job_basics.reporting_to": True,
    "job_basics.location": True,
    "job_basics.remote_option": True,
    "job_basics.travel_requirement": True,
    # 🔹 Skills & Experience
    "education.education_level": True,
    "education.certifications_required":True,
    "education.education_fields": True,
    "experience.experience_years":True,
    "experience.experience_domains": True,
    "skills.hard_skills": True,
    "skills.soft_skills": True,
    "skills.tools_platforms": True,
    "skills.languages_required": True,
    # 🔹 Strategic & Performance Focus
    "role_reponsibility.reponsibilities": True,
    "role_reponsibility.strategic_goals": True,
    "role_reponsibility.performance_indicators": True,
    "role_reponsibility.leadership_expectations": True,
    "role_reponsibility.transformation_initiatives": True,
    # 🚫 Metadata (excluded from embeddings)
    "job_basics.start_date": False,
    "job_basics.job_reference_id": False,
    "compensation_timeline.posting_date": False,
    "compensation_timeline.application_deadline": False,
    "compensation_timeline.salary_range": False,
    "experience.project_examples": False,
    "application_process.application_mode": False,
    "application_process.application_requirements": False,
    "application_process.interview_stages": False,
    "application_process.selection_criteria": False,
    "team_collaboration.cross_functional": False,
    "team_collaboration.internal_collaboration": False,
    "team_collaboration.external_stakeholders": False,
    "team_collaboration.team_size": False,
    "role_reponsibility.decision_making_scope": False,
    "role_reponsibility.personal_traits": False,
    "role_reponsibility.success_metrics": False,
    "growth_career.learning_opportunities": False,
    "growth_career.career_path": False,
    "legal_eligibility.legal_eligibility": False,
    "legal_eligibility.work_authorization": False,
    "legal_eligibility.relocation_support": False,
    "company_culture.employer_name": False,
    "company_culture.mission_focus": False,
    "company_culture.company_culture": False,
    "company_culture.diversity_inclusion": False,
    "company_culture.employer_type":False
}



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



job_posting_relevant  = fetch_relevant_info(job_posting, embedding_field_config)
with open("./archives/job_posting_relevant.txt", "w", encoding="utf-8") as f:
    json.dump(job_posting_relevant, f, indent=2)


reconstructed_job_posting = reconstruct_job_posting(job_posting_relevant)
with open("./archives/reconstructed_job_posting.txt", "w", encoding="utf-8") as f:
    json.dump(reconstructed_job_posting, f, indent=2)


from pprint import pprint

reconstructed_job_posting_obj = JobPosting(**job_posting)
 


from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

flat_fields =flatten_fields(reconstructed_job_posting_obj.model_dump())
with open("./archives/flat_fields.txt", "w", encoding="utf-8") as f:
    json.dump(flat_fields, f, indent=2)


count = 0
delay = 60
for i in range(len(flat_fields)):
    # print(embeddings[i]["field_path"])
    # print(embeddings[i]["original_text"])
    field_path = flat_fields[i][0]
    original_text = flat_fields[i][1]
    # print(field_path, original_text)
    try:
        print(f'Finding similar terms for: {original_text}')
        similar_terms = get_similar_terms_from_llm(original_text, api_key="")
        similar_terms = cleanup_llm_output(raw_output=similar_terms)
        for term in similar_terms:
            flat_fields.append([field_path, term])
    except Exception as e:
        print(f"Error getting similar terms for {original_text}: {e}")
        count+=1
        print('Waiting for a minute')
        time.sleep(delay)
        i = i-1

embeddings = embed_field_values(model,flat_fields)
with open("./archives/embeddings.txt", "w", encoding="utf-8") as f:
    json.dump(embeddings, f, indent=2)





    #         try:
    #             similar_terms = get_similar_terms_from_llm(text, GOOGLE_API_KEY)
    #             similar_terms = [text]+cleanup_llm_output(raw_output=similar_terms)
    #             field_dict[text] = similar_terms
    #         except Exception as e:
    #             print(f"Error getting similar terms for {text}: {e}")
    #             field_dict[text] = []  # fallback to empty list if something fails
    # if field_dict:
    #     fields_with_similar_terms[field] = [field_dict]

# pprint(reconstructed_job_posting_obj)
# field_embeddings_info = get_embedding_fields_with_type(reconstructed_job_posting_obj, embedding_field_config)

# pprint(field_embeddings_info)

# with open("field_embeddings_info.txt", "w", encoding="utf-8") as f:
#     json.dump(field_embeddings_info, f, indent=2)




# ###################################################################################################################
#                                         # Do not delete this code
# ###################################################################################################################

# # fields_with_similar_terms = {}

# # for field, items in field_embeddings_info.items():
# #     field_dict = {}
# #     for text, text_type in items:
# #         if text_type in ['word', 'word_phrase', 'sentence']:
# #             try:
# #                 similar_terms = get_similar_terms_from_llm(text, GOOGLE_API_KEY)
# #                 similar_terms = [text]+cleanup_llm_output(raw_output=similar_terms)
# #                 field_dict[text] = similar_terms
# #             except Exception as e:
# #                 print(f"Error getting similar terms for {text}: {e}")
# #                 field_dict[text] = []  # fallback to empty list if something fails
# #     if field_dict:
# #         fields_with_similar_terms[field] = [field_dict]

# # pprint(fields_with_similar_terms)
# # with open("fields_with_similar_terms.txt", "w", encoding="utf-8") as f:
# #     json.dump(fields_with_similar_terms, f, indent=2)


# # using this for time being as qouta is vertisch
# with open('fields_with_similar_terms.txt', "r", encoding="utf-8") as f:
#     content = f.read()
#     fields_with_similar_terms = ast.literal_eval(content)

# ###################################################################################################################
#                                         # Do not delete this code
# ###################################################################################################################




# model = SentenceTransformer("all-MiniLM-L6-v2")

# embedded_terms_dict = {}

# # Loop through the outer fields
# for field, field_entries in fields_with_similar_terms.items():
#     embedded_entries = []
#     for entry_dict in field_entries:
#         embedded_entry_dict = {}
#         for term, similar_terms in entry_dict.items():
#             all_terms_for_key = [term] + similar_terms
#             # Compute embeddings for the term list
#             embeddings = model.encode(similar_terms, convert_to_numpy=True).tolist()
#             embedded_entry_dict[term] = embeddings
#         embedded_entries.append(embedded_entry_dict)
#     embedded_terms_dict[field] = embedded_entries


# # pprint(embedded_entries)

# # Save to a text file as pretty JSON
# with open("embedded_terms_dict.txt", "w", encoding="utf-8") as f:
#     json.dump(embedded_terms_dict, f, indent=2)