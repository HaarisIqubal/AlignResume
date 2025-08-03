import requests
from bs4 import BeautifulSoup
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from src.tool.job_extractor import extract_job_detail
from JobPosting import JobPosting

parser = PydanticOutputParser(pydantic_object=JobPosting)

format_instructions  = parser.get_format_instructions()

def fetch_job_posting_text(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator="\n")

def build_langchain_chain():
    # parser = JsonOutputParser(pydantic_object=JobPosting)
    parser = StrOutputParser()
    prompt = PromptTemplate(
        template="""
You are an information extraction engine. Extract the job posting data according to the following schema:

{format_instructions}

Job Posting:
{job_text}
""",
        input_variables=["job_text","format_instructions"],
        # partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    llm = ChatOllama(model="gemma3n:latest", num_predict=128, disable_streaming=False)
    chain = prompt | llm | parser
    return chain

def process_job_posting(url: str):
    # print("Fetching job posting text...")
    # job_text = fetch_job_posting_text(url)

    job_text = extract_job_detail(url)

    print(job_text)

    print("Running through LangChain...")
    chain = build_langchain_chain()
    # job_posting = chain.invoke({"job_text": job_text})

    streamed_output = ""
    for chunk in chain.stream({"job_text": job_text,"format_instructions":format_instructions}):
        print(chunk,end="", flush=True)
        streamed_output+=chunk



    print("\n✅ Structured Job Posting:")
    print(streamed_output.json(indent=2))

if __name__ == "__main__":
    job_url = input("Enter job posting URL: ").strip()
    process_job_posting(job_url)
