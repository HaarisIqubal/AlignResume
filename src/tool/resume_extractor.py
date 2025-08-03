import json
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from ..model.ResumeSchema import Personal
from .llm_manager import llm_manager

def extract_resume_detail(raw_data: str) -> Personal:
    """
    Extract structured resume information using LLM.
    Parameters
    ----------
    resume_data_data : str
        The string of raw extracted data from the pdf.

    Returns
    -------
    resume_model : Personal
            This will return the value of personal in formatted way of pydantic.
    """
    prompt = PromptTemplate(
    template="""Extract structured information from the following resume and return it as a JSON object.
    Resume:
    {resume_text}
    {format_instructions}
    Only return valid JSON, no explanations.""",
        input_variables=["resume_text","format_instructions"]
    )
    parser = PydanticOutputParser(pydantic_object=Personal)
    chain = llm_manager.init_llm_chain(prompt=prompt)

    try:
        raw_output = chain.invoke({"resume_text": raw_data,
                                    "format_instructions": parser.get_format_instructions()})
        raw_output = llm_manager.cleanup_llm_output(raw_output)
        parsed_json = json.loads(raw_output)
        resume_model = Personal(**parsed_json)
        return resume_model
    except Exception as e:
        print(f"Exception {e}")
        return Personal(name="None", email="None", phone="None", education=[],experience=[])
    finally:
        print("Finally passed")
