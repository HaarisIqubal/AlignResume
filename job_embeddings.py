'''
| Goal                | Best Fields to Embed Eg.                         |
| ------------------- | ---------------------------------------------- |
| **CV–job matching** | skills, experience, responsibilities, values   |
| **Job clustering**  | department, mission, strategic goals           |
| **Search/filter**   | include more general text, less personal match |

'''

from src.model.JobPostingSchema import JobPosting
from src.model.ResumeSchema import Personal 
from src.tool.embedding_util import cleanup_llm_output, fetch_relevant_info, reconstruct_job_posting, flatten_fields, embed_field_values, transform_input_to_output_with_llm
from sentence_transformers import SentenceTransformer
import json
import time 

job_posting = { 
    "job_basics": { "job_title": "Purchasing Framework, Digitalization & Risk Managment professional", "department": "Strategy & Business Development", "job_type": "Full-Time", "start_date": None, "location": "Thailand (implied by contact info)", "remote_option": None, "travel_requirement": None, "reporting_to": None, "job_reference_id": None }, "education": { "education_level": None, "education_fields": [], "certifications_required": [] }, "experience": { "education_level": "At least 3 years of experience", "education_fields": [ "Purchasing or equivalent", "network organization" ], "certifications_required": [] }, "skills": { "hard_skills": [ "Project management methods", "Data and Performance Management", "Risk Management (supply chain, delivery, financial, regulatory)", "Risk mitigation strategies", "Analytical skills", "Conceptual skills" ], "soft_skills": [ "Continuous Improvement", "Collaboration", "Capabilities improvement", "High proficiency in verbally and written Communicating skills on an international basis", "High ability and willingness to approach other persons and cultures in an unbiased and open manner", "Ability to work with diverse opinions and expectations", "Good interpersonal skills", "Curious", "Open minded", "Agility to engage people", "Good organizational and planning skills", "Independent working style", "Strategic thinking", "Takes the initiative", "Think out of the box", "Understand easily complex business matters", "Ability to deliver results under pressure", "Team player attitude", "Friendly", "Service oriented", "Independent and responsible way of working", "Quick comprehension", "Assertiveness" ], "tools_platforms": [], "languages_required": [ "English (written and spoken)" ] }, "role_reponsibility": { "responsibilities": [ "Continuous Improvement and improvement projects management", "Identify areas within the purchasing process that can be optimized for efficiency and cost-effectiveness", "Support to conduct regular reviews of purchasing activities to identify improvement opportunities", "Conducting necessary project management methods within the defined purchasing processes & systems by defining relevant objectives, collecting datas, excecution and contibuting to its long term success", "Support the Data and Performance Management team to define areas of improvement within the existing reporting and data management", "Support the management to assess the skills and capabilities of the purchasing team and identify areas for development", "Propose performance improvement plans, onboarding plans etc. with the collaboration with HR and QPP", "Ensure the accessibility and inortmation sharing of the trainings, tools and processes to the Purchasing teams in Asia Pacific", "Facilitate effective communication and collaboration between the purchasing team and other departments", "Participate in cross-functional projects and initiatives to drive overall business success", "Stay abreast of industry trends and emerging technologies that can enhance purchasing operations", "Foster a culture of innovation by encouraging team members to propose and implement new ideas", "Collaborate with Purchasing teams and other departments to support the integration of innovative solutions", "Identify potential risks in the supply chain, such delivery Risks, Financial risks etc. and regulatory changes", "Develop and implement risk mitigation strategies to minimize the impact of identified risks", "Monitor the external environment for emerging risks and adjust strategies accordingly" ], "performance_indicators": [], "personal_traits": [ "Curious", "Open minded", "Agility to engage people", "Independent working style", "Strategic thinking", "Takes the initiative", "Think out of the box", "Team player attitude", "Friendly", "Service oriented", "Independent and responsible way of working", "Assertiveness" ], "strategic_goals": [ "Drive overall business success", "Contribute to sustainable value creation for our stakeholders and society as a whole", "Advance how the world moves" ], "transformation_initiatives": [], "success_metrics": [], "leadership_expectations": "Information on leadership understanding is referred to schaeffler.com/leadership.", "decision_making_scope": None }, "legal_eligibility": { "legal_eligibility": None, "work_authorization": None, "relocation_support": None }, "company_culture": { "employer_name": "Schaeffler", "employer_type": "dynamic global technology company", "company_culture": [ "Entrepreneurial spirit", "Long history of private ownership", "Treat each other with respect", "Value all ideas and perspectives", "Appreciating our differences", "Inspire creativity and drive innovation" ], "mission_focus": [ "Partner to all of the major automobile manufacturers", "Partner to key players in the aerospace and industrial sectors", "Impact the future with innovation", "Advance how the world moves", "Sustainable value creation for our stakeholders and society as a whole" ], "diversity_inclusion": "As a global company with employees around the world, it is important to us that we treat each other with respect and value all ideas and perspectives. By appreciating our differences, we inspire creativity and drive innovation." }, "application_process": { "application_mode": None, "application_requirements": [], "interview_stages": None, "selection_criteria": [] }, "compensation_timeline": { "salary_range": None, "posting_date": None, "application_deadline": None }, "team_collaboration": { "team_size": None, "cross_functional": True, "internal_collaboration": [ "Facilitate effective communication and collaboration between the purchasing team and other departments", "Collaborate with Purchasing teams and other departments to support the integration of innovative solutions" ], "external_stakeholders": [] }, "growth_career": { "learning_opportunities": [ "Many development opportunities", "Assess the skills and capabilities of the purchasing team and identify areas for development", "Propose performance improvement plans, onboarding plans", "Ensure the accessibility and information sharing of the trainings, tools and processes" ], "career_path": "Exciting assignments and outstanding development opportunities await you" } }

resume_data = {
  "name": "Shubham Gupta",
  "email": "g.shubham1@outlook.com",
  "phone": "(+49) 15510186370",
  "education": [
    {
      "degree": "Bachelor of Technology - Computer Science and Engineering",
      "institution": "Vellore Institute of Technology",
      "start_data": "1 Jul 2016",
      "end_data": "Apr 2020",
      "education_field": "Computer Science and Engineering"
    },
    {
      "degree": "M.Sc. - Data Science",
      "institution": "Friedrich-Alexander University Erlangen-Nuremberg",
      "start_data": "16 Oct 2023",
      "end_data": "Current",
      "education_field": "Data Science"
    }
  ],
  "experience": [
    {
      "title": "Part-time Data Scientist",
      "company": "Siemens Healthineers Treasury",
      "start_date": "June 2024",
      "end_date": "Present",
      "description": "Collaborated with various finance teams and worked on creating a centralized data catalog using Snowflake, improving data accessibility to business users using Power BI. Researched business viability of using LLMs like transformer architecture for time series forecasting by using Foundational Models like TimeGPT, Chronos. Researched and implemented liquidity forecasting using LSTM and other Deep Learning Models, leveraging PyTorch and TensorFlow. Replicated LSTM based on recent research approaches to improve the liquidity forecast at enterprise level. Analyzed various time-series libraries such as Orbit, Prophet, pmdarima, darts, and pytorchts to find the best fit for the use case.",
      "experience_domain": [
        "Data Science",
        "Finance",
        "Treasury",
        "Digitalization",
        "Data Cataloging",
        "Business Intelligence",
        "LLMs",
        "Time Series Forecasting",
        "Deep Learning",
        "Financial Modeling"
      ]
    },
    {
      "title": "Software Development Engineer",
      "company": "Tata Consultancy Services Limited (TCS)",
      "start_date": "Sep 2020",
      "end_date": "Sep 2023",
      "description": "Developed a web application with Java Web Technologies to create an AD group analysis tool with a Single Sign-On (SSO) feature, reducing process time by 30%. Worked as part of the DevOps team, deploying various enhancements in collaboration with the Development Team. Increased efficiency, reduced manual efforts, resulted in $25K annual cost saving.",
      "experience_domain": [
        "Software Development",
        "Web Development",
        "Java",
        "DevOps",
        "Automation",
        "Process Improvement"
      ]
    },
    {
      "title": "Backend Web Developer",
      "company": "Tata Consultancy Services Limited (TCS)",
      "start_date": "Sep 2020",
      "end_date": "Sep 2023",
      "description": "Developed a web application in Java using Spring Boot to manage employee competencies and a dashboard to enhance user skills. The application used a monolithic architecture with Liquidbase for database transactions, Hibernate as an ORM, and a GitHub Actions pipeline to deploy the application on Azure Cloud. Other skills learned: SQL, GitHub, Agile Methodology.",
      "experience_domain": [
        "Backend Web Development",
        "Java",
        "Spring Boot",
        "Database Management",
        "Cloud Deployment",
        "DevOps",
        "Agile Methodologies"
      ]
    },
    {
      "title": "Data Scientist",
      "company": "Tata Consultancy Services Limited (TCS)",
      "start_date": "Sep 2020",
      "end_date": "Sep 2023",
      "description": "Developed and deployed similarity-based (cosine similarity, Euclidean distance) and clustering (k-median) algorithms for an MVP using Python libraries and MLFlow. Collaborated with the team to implement MLOps using MLFlow, where deployed models were constantly monitored and retrained based on new data from vendors via ETL pipelines. Analyzed, mined, and visualized data received from vendors in QlikSense for better business decisions.",
      "experience_domain": [
        "Data Science",
        "Machine Learning",
        "MLOps",
        "Data Analysis",
        "Data Visualization",
        "ETL"
      ]
    },
    {
      "title": "Machine Learning Intern - NLP",
      "company": "Tata Consultancy Services Limited (TCS)",
      "start_date": "Jan 2020",
      "end_date": "Mar 2020",
      "description": "Effectively enhanced system performance. Major responsibilities included data collection and feature selection. Contributed to the model selection process. Researched various classical NLP methods like Tokenization, Lemmatization and Stemming. Implemented Bag-of-Words and TF-IDF for feature extraction.",
      "experience_domain": [
        "Machine Learning",
        "Natural Language Processing (NLP)",
        "Data Collection",
        "Feature Engineering",
        "Model Selection"
      ]
    }
  ],
  "total_experience": {
    "experience_years": "3 years 4 months",
    "experience_domains": [
      "Data Science",
      "Finance",
      "Treasury",
      "Digitalization",
      "Data Cataloging",
      "Business Intelligence",
      "LLMs",
      "Time Series Forecasting",
      "Deep Learning",
      "Financial Modeling",
      "Software Development",
      "Web Development",
      "Java",
      "DevOps",
      "Automation",
      "Process Improvement",
      "Backend Web Development",
      "Database Management",
      "Cloud Deployment",
      "Agile Methodologies",
      "Machine Learning",
      "MLOps",
      "Data Analysis",
      "Data Visualization",
      "ETL",
      "Natural Language Processing (NLP)",
      "Data Collection",
      "Feature Engineering",
      "Model Selection"
    ],
    "project_examples": [
      "Climate Change and Its Burn on Pocket - Cost of Living Crisis",
      "Point Prevalence Analysis App for Infectious Disease Stewardship",
      "ToolAct - X-AI way to understand Time Series Classification"
    ]
  },
  "skills": {
    "hard_skills": [
      "Python",
      "Java",
      "SQL",
      "LLMs",
      "Fine-Tuning",
      "RAG",
      "Time Series Forecasting",
      "Deep Learning",
      "Machine Learning",
      "NLP",
      "Data Manipulation",
      "Data Analysis",
      "Data Visualization",
      "ETL",
      "Web Development",
      "Monolithic Architecture",
      "ORM",
      "SSO",
      "Agile Methodology",
      "Project Planning",
      "CI/CD",
      "Automated Testing",
      "Statistical Analysis",
      "Algorithm Development",
      "Feature Engineering",
      "Data Collection",
      "Model Selection",
      "Research",
      "Business Viability Analysis",
      "Tokenization",
      "Lemmatization",
      "Stemming",
      "Bag-of-Words",
      "TF-IDF",
      "Cosine Similarity",
      "Euclidean Distance",
      "Clustering (k-median)"
    ],
    "soft_skills": [
      "Collaboration",
      "Research",
      "Problem-solving",
      "Efficiency",
      "Automation",
      "Communication",
      "Business Acumen"
    ],
    "tools_platforms": [
      "GitLab",
      "GitHub",
      "GitHub Actions",
      "Docker",
      "TensorFlow",
      "Keras",
      "PyTorch",
      "Scikit-Learn",
      "NumPy",
      "Matplotlib",
      "MLFlow",
      "Azure (AI Studio)",
      "AWS (Bedrock)",
      "Langchain",
      "Pinecone",
      "Hugging Face",
      "Streamlit",
      "Snowflake",
      "Power Query",
      "Power BI",
      "QlikSense",
      "Spring Boot",
      "Liquidbase",
      "Hibernate",
      "TimeGPT",
      "Chronos",
      "Orbit",
      "Prophet",
      "pmdarima",
      "darts",
      "pytorchts",
      "Jira",
      "Confluence",
      "Microsoft Office"
    ],
    "languages_required": [
      "Deutsch (A2)",
      "English (C1)"
    ]
  },
  "responsibilities": {
    "responsibilities": [
      "Collaborating with cross-functional teams (finance, development, infectious disease specialists)",
      "Developing and deploying data science and software solutions",
      "Conducting research on emerging technologies (LLMs, X-AI, Deep Learning)",
      "Implementing MLOps practices for model monitoring and retraining",
      "Analyzing and visualizing data for business insights",
      "Improving efficiency and reducing costs through automation",
      "Translating complex requirements into technical features",
      "Data collection and feature selection",
      "Contributing to model selection processes"
    ],
    "personal_traits": [],
    "transformation_initiatives": [],
    "leadership_expectations": None,
    "decision_making_scope": None
  }
}

job_post_field_config = {
    # 🔹 Role & Responsibility
    "job_basics.job_title": True,
    "job_basics.department": True,
    "job_basics.job_type": True,
    "job_basics.reporting_to": False,
    "job_basics.location": True,
    "job_basics.remote_option": False,
    "job_basics.travel_requirement": False,
    # Skills & Experience
    "education.education_level": True,
    "education.certifications_required":True,
    "education.education_fields": True,
    "experience.experience_years":True,
    "experience.experience_domains": True,
    "skills.hard_skills": True,
    "skills.soft_skills": True,
    "skills.tools_platforms": True,
    "skills.languages_required": True,
    # Strategic & Performance Focus
    "role_reponsibility.reponsibilities": True,
    "role_reponsibility.strategic_goals": False,
    "role_reponsibility.performance_indicators": False,
    "role_reponsibility.leadership_expectations": True,
    "role_reponsibility.transformation_initiatives": True,
    # Metadata (excluded from embeddings)
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

resume_field_config = {
    # ✅ Experience
    "experience.title": True,
    "experience.previous_job_titles": True,
    "experience.experience_domain": True,
    "experience.company": False,
    "experience.start_date": False,
    "experience.end_date": False,
    "experience.description": True,
    "experience.keywords": True,

    # ✅ Total Experience
    "total_experience.experience_domains": True,
    "total_experience.experience_years": True,
    "total_experience.certifications": True,
    "total_experience.project_examples": False,

    # ✅ Education
    "education.degree": True,
    "education.education_field": True,
    "education.institution": False,
    "education.start_data": False,
    "education.end_data": False,

    # ✅ Skills
    "skills.hard_skills": True,
    "skills.soft_skills": True,
    "skills.tools_platforms": True,
    "skills.languages_required": True,

    # ✅ Responsibilities
    "responsibilities.responsibilities": True,
    "responsibilities.leadership_expectations": True,
    "responsibilities.decision_making_scope": True,
    "responsibilities.personal_traits": False,
    "responsibilities.transformation_initiatives": False,
    # "responsibilities.performance_indicators": True,       # ➕ Add to model if needed
    # "responsibilities.success_metrics": True,              # ➕ Add to model if needed

    # ✅ Personal
    "personal.name": False,
    "personal.email": False,
    "personal.phone": False,
    "personal.education": False,
    "personal.experience": True,
    "personal.total_experience": True,
    "personal.skills": True,
    "personal.responsibilities": False,
    # "personal.legal_eligibility": True,                    # ➕ If you plan to add it
    # "personal.location_preference": True,                  # ➕ If you plan to add it
    # "personal.professional_traits": True,                  # ➕ If you plan to add it
    # "personal.learning_opportunities": True,               # ➕ If you plan to add it
    # "personal.career_growth": True,                        # ➕ If you plan to add it
    # "personal.salary_expectations": True,                  # ➕ If you plan to add it
    # "personal.available_from": True,                       # ➕ If you plan to add it
    # "personal.application_deadline": True,                 # ➕ If you plan to add it

    # ✅ Team Collaboration
    "team_collaboration.team_size": True,
    "team_collaboration.cross_functional": True,
    "team_collaboration.internal_collaboration": True,
    "team_collaboration.external_stakeholders": True
}



job_posting_relevant  = fetch_relevant_info(job_posting, job_post_field_config)
with open("./archives/job_posting_relevant.txt", "w", encoding="utf-8") as f:
    json.dump(job_posting_relevant, f, indent=2)

reconstructed_job_posting = reconstruct_job_posting(job_posting_relevant)
with open("./archives/reconstructed_job_posting.txt", "w", encoding="utf-8") as f:
    json.dump(reconstructed_job_posting, f, indent=2)

reconstructed_job_posting_obj = JobPosting(**reconstructed_job_posting)
flat_fields_job_posting =flatten_fields(reconstructed_job_posting_obj.model_dump())
with open("./archives/flat_fields_job_posting.txt", "w", encoding="utf-8") as f:
    json.dump(flat_fields_job_posting, f, indent=2)


resume_relevant  = fetch_relevant_info(resume_data, resume_field_config)
with open("./archives/resume_relevant.txt", "w", encoding="utf-8") as f:
    json.dump(resume_relevant, f, indent=2)

reconstructed_resume = reconstruct_job_posting(resume_relevant)
with open("./archives/reconstructed_resume.txt", "w", encoding="utf-8") as f:
    json.dump(reconstructed_resume, f, indent=2)


reconstructed_resume_obj = Personal(**reconstructed_resume)
flat_fields_resume =flatten_fields(reconstructed_resume_obj.model_dump())
with open("./archives/flat_fields_resume.txt", "w", encoding="utf-8") as f:
    json.dump(reconstructed_resume_obj.model_dump(), f, indent=2)

model = SentenceTransformer("all-MiniLM-L6-v2")

# api_key="AIzaSyBbUhKXtXlGlEyu4Li-ytdoDac0fN2HmLI"
# new_output_data = transform_input_to_output_with_llm(input_format = flat_fields_job_posting)

# print(new_output_data[0])
# ['job_basics.job_title', ['Purchasing Framework, Digitalization & Risk Managment professional', 'Procurement strategy', 'Digital transformation', 'Risk assessment', 'Supply chain risk', 'Vendor management', 'E-procurement', 'Business process automation', 'Compliance management', 'Enterprise risk', 'Strategic sourcing']]

print(type(flat_fields_job_posting))
print(flat_fields_job_posting[0])


print(type(flat_fields_resume))
print(flat_fields_resume[0])



# embeddings_job_post = embed_field_values(model,flat_fields_job_posting)
# with open("./archives/embeddings_job_post.txt", "w", encoding="utf-8") as f:
#     json.dump(embeddings_job_post, f, indent=2)

# embeddings_resume = embed_field_values(model,flat_fields_resume)
# with open("./archives/embeddings_resume.txt", "w", encoding="utf-8") as f:
#     json.dump(embeddings_resume, f, indent=2)


