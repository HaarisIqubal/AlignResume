from src.model.JobPostingSchema import JobPosting
from src.tool.llm_manager import llm_manager
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import PromptTemplate
import ast
import time


# def is_single_word(text: str) -> bool:
#     return len(text.strip().split()) == 1 and text.strip().isalpha()

# def is_keyword_phrase(text: str) -> bool:
#     words = text.strip().split()
#     return 2 <= len(words) <= 4 and all(w.isalpha() for w in words)

# def is_full_phrase(text: str) -> bool:
#     return len(text.strip().split()) > 4 or not text.replace(" ", "").isalpha()

# def classify_text_type(text: str) -> str:
#     if is_single_word(text):
#         return "word"
#     elif is_keyword_phrase(text):
#         return "word_phrase"
#     else:
#         return "sentence"

# def get_embedding_fields_with_type(job_posting: JobPosting, config: dict) -> dict:
#     field_type_map = {}
#     for field, use in config.items():
#         if not use:
#             continue
#         value = getattr(job_posting, field, None)

#         if not value:
#             continue

#         # Handle lists
#         if isinstance(value, list):
#             for item in value:
#                 if isinstance(item, str) and item.strip():
#                     text_type = classify_text_type(item)
#                     field_type_map.setdefault(field, []).append((item, text_type))

#         # Handle strings
#         elif isinstance(value, str) and value.strip():
#             text_type = classify_text_type(value)
#             field_type_map[field] = [(value, text_type)]

#     return field_type_map

def get_similar_terms_from_llm(term: str, api_key: str) -> list[str]:
    prompt = PromptTemplate(
    template="""You are a helpful assistant. For the term '{term}', generate a list of 10 closely related words or short phrases. These should capture synonyms, related job titles, and conceptually similar terms. Avoid full sentences. Keep short phrases. Make sure you do not leave anything empty. Only return a Python list of strings.""",
        input_variables=["term"]
    )
    
    parser = StrOutputParser()
    chain = llm_manager.init_llm_chain(prompt=prompt)
    try:
        sim_word_list = chain.invoke({"term": term})
        return sim_word_list
    except Exception as e:
        print(f"Exception {e}")
        return 
    finally:
        print("Finally passed")




# def get_similar_terms_from_llm(term: str, api_key: str, retries: int = 3, delay: int = 60) -> list[str]:
#     prompt = PromptTemplate(
#         template=(
#             "You are a helpful assistant. For the term '{term}', generate a list of 10 closely related words or short phrases. "
#             "These should capture synonyms, related job titles, and conceptually similar terms. Avoid full sentences. Keep short phrases. "
#             "Make sure you do not leave anything empty. Only return a Python list of strings."
#         ),
#         input_variables=["term"]
#     )

#     parser = StrOutputParser()
    
#     # Initialize the chain once
#     try:
#         chain = llm_manager.init_llm_chain(prompt=prompt)
#     except Exception as e:
#         print(f"Failed to initialize LLM chain: {e}")
#         return []

#     for attempt in range(1, retries + 1):
#         try:
#             sim_word_list = chain.invoke({"term": term})
            
#             # Validate output
#             if isinstance(sim_word_list, str):
#                 # Attempt to safely evaluate the string into a list
#                 import ast
#                 sim_word_list = ast.literal_eval(sim_word_list)

#             if not isinstance(sim_word_list, list):
#                 raise ValueError("LLM response is not a list.")

#             return sim_word_list

#         except Exception as e:
#             print(f"Attempt {attempt} failed for term '{term}': {e}")
#             if attempt < retries:
#                 time.sleep(delay)
#             else:
#                 print(f"All {retries} attempts failed for term '{term}'")
#                 return []

#         finally:
#             print(f"Finished attempt {attempt} for term '{term}'")


def cleanup_llm_output(raw_output: str) -> str:
        """Clean up LLM output to extract pure JSON"""
        if raw_output.startswith("```python"):
            raw_output = raw_output[len("```python"):].lstrip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].rstrip()
        raw_output = raw_output.strip()
        word_list = ast.literal_eval(raw_output)
        return word_list


def fetch_relevant_info(job_posting, embedding_field_config):
    # Split the field config and access the nested fields using recursion
    def get_value_from_nested_dict(nested_dict, keys):
        # Iterate over keys and get the value from the nested structure
        for key in keys:
            if key in nested_dict:
                nested_dict = nested_dict[key]
            else:
                return None
        return nested_dict

    relevant_info = {}
    for field, include in embedding_field_config.items():
        if include:  # Only include fields marked as True
            keys = field.split('.')  # Split the field path into keys
            value = get_value_from_nested_dict(job_posting, keys)
            if value is not None:
                relevant_info[field] = value

    return relevant_info

def reconstruct_job_posting(relevant_info):
    # Initialize the base structure of the job posting
    job_posting_reconstructed = {}

    def set_nested_value(nested_dict, keys, value):
        # This function will set the value in the correct place of the nested dictionary
        for key in keys[:-1]:  # Traverse all but the last key
            if key not in nested_dict:
                nested_dict[key] = {}
            nested_dict = nested_dict[key]
        nested_dict[keys[-1]] = value

    for field, value in relevant_info.items():
        keys = field.split('.')  # Split the field path into keys
        set_nested_value(job_posting_reconstructed, keys, value)

    return job_posting_reconstructed


def extract_values_from_object(obj):
    values = {}

    def extract(obj, parent_key=""):
        # If the object is a list, process each element
        if isinstance(obj, list):
            values[parent_key] = ", ".join(map(str, obj))
        # If the object is a dictionary, recurse into its items
        elif isinstance(obj, dict):
            for key, value in obj.items():
                extract(value, f"{parent_key}.{key}" if parent_key else key)
        # If the object is a basic type (string, int, etc.), directly add it
        else:
            values[parent_key] = str(obj)

    # Start extracting values from the root object
    extract(obj)
    return values



def flatten_fields(data, prefix=""):
    flat_fields = []
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat_fields.extend(flatten_fields(value, path))
        elif isinstance(value, list):
            for item in value:
                flat_fields.append((path, item))
        elif value:  # ignore None/empty
            flat_fields.append((path, value))
    return flat_fields

def embed_field_values(model, flat_fields):
    embedded = []
    for path, text in flat_fields:
        if isinstance(text, str) and text.strip():
            vector = model.encode(text)
            embedded.append({
                "field_path": path,
                "original_text": text,
                "embedding": vector.tolist()  # convert numpy to list for JSON saving
            })
    return embedded