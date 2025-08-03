import json
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from langchain.schema.output_parser import StrOutputParser
from ..model.resume_schema import Personal

def extract_resume_detail(resume_raw_data: str) -> Personal:
    """Extract structured resume information using LLM"""
    prompt = PromptTemplate(
    template="""Extract structured information from the following resume and return it as a JSON object.
    Resume:
    {resume_text}
    {format_instructions}
    Only return valid JSON, no explanations.""",
        input_variables=["resume_text","format_instructions"]
    )
    parser = PydanticOutputParser(pydantic_object=Personal)
    chain = _init_ollama_llm(prompt=prompt)

    try:
        raw_output = chain.invoke({"resume_text": resume_raw_data,
                                    "format_instructions": parser.get_format_instructions()})
        raw_output = _cleanup_llm_output(raw_output)
        parsed_json = json.loads(raw_output)
        resume_model = Personal(**parsed_json)
        return resume_model
    except Exception as e:
        print(f"Exception {e}")
        return Personal(name="None", email="None", phone="None", education=[],experience=[])
    finally:
        print("Finally passed")


def _init_ollama_llm(prompt: PromptTemplate) -> Runnable:
    """Initialize Ollama LLM with prompt chain"""
    language_model = ChatOllama(model="gemma3n:e4b", temperature=0)
    chain:Runnable = prompt | language_model | StrOutputParser()
    return chain

def _cleanup_llm_output(raw_output: str) -> str:
    """Clean up LLM output to extract pure JSON"""
    if raw_output.startswith("```json"):
        raw_output = raw_output[len("```json"):].lstrip()
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3].rstrip()
    return raw_output.strip()