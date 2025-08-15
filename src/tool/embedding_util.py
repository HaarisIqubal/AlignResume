
from src.tool.llm_manager import llm_manager
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import PromptTemplate
import ast
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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

def get_similar_terms_from_llm(input_list: list, api_key: str, similar_k=10) -> list[list]:
    prompt = PromptTemplate(
    # template="""You are a helpful assistant. For the term '{term}', generate a list of 5 closely related words or short phrases. These should capture synonyms, related job titles, and conceptually similar terms. Avoid full sentences. Keep short phrases. Make sure you do not leave anything empty. Only return a Python list of strings.""",
    #     input_variables=["term"]

    template = f"""
    You are a meticulous data wrangler. Your job is to transform an input list of [key, value] pairs into a FLAT output list.
    For each input pair (key, value) in the {input_list}, emit a block of {similar_k + 1} rows in this order:
    1) [key, value]    # original value verbatim
    2) [key, sim1]
    3) [key, sim2]
    ...
    {similar_k + 1}) [key, sim{similar_k}]

    IMPORTANT KEY RULES (MUST FOLLOW EXACTLY):
    - Keys MUST be copied VERBATIM from the input. Do not add, remove, or alter any characters.
    - Never invent new keys, never duplicate substrings, never change separators or casing.
    - If a key is 'skills.soft_skills', every row in that block MUST have 'skills.soft_skills' as the key.

    "Similar words" means concise synonyms or closely related terms for the entire value phrase (domain-relevant skills, functions, tools, or concepts). Optimize for usefulness in search/matching.

    STRICT RULES:
    1) Output MUST be valid, minified JSON only. No comments, no prose, no code fences.
    2) For EACH input pair, output EXACTLY {similar_k + 1} rows: first the original value (verbatim), then {similar_k} distinct, high-quality similar terms.
    3) Terms: keep each ≤3 words; avoid duplicates; avoid acronyms-only entries unless widely recognized.
    4) Use American English; Title Case only for proper nouns; otherwise sentence case is fine.
    5) If a value has multiple themes, distribute the similar terms across those themes.
    6) No filler words (e.g., "etc."), no meaningless numbers. Include standards (e.g., "ISO 31000") only if clearly relevant.
    7) Preserve the original value text verbatim for the first row of each block.
    8) Preserve the exact input order: the output must be blocks in the same order as the input pairs.

    Return JSON ONLY in this exact structure (FLAT list):
    [
    [key1, value1],
    [key1, sim1],
    [key1, sim2],
    ...
    [key1, sim{similar_k}],
    [key2, value2],
    [key2, sim1],
    ...
    [key2, sim{similar_k}],
    ...
    ]
    Here is input_format:
    {input_list}
    """.strip(),
    input_variables=["input_list"]
    )
    parser = StrOutputParser()
    chain = llm_manager.init_llm_chain(prompt=prompt)
    try:
        output_format = chain.invoke({"input_list": input_list})
        # print('1St line')
        # print(output_format)
        output_format = cleanup_llm_output_json(output_format)
        return output_format
    except Exception as e:
        print(f"Exception {e}")
        return 
    finally:
        print("Finally passed")



def cleanup_llm_output(raw_output: str) -> str:
        """Clean up LLM output to extract pure JSON"""
        if raw_output.startswith("```python"):
            raw_output = raw_output[len("```python"):].lstrip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].rstrip()
        raw_output = raw_output.strip()
        word_list = ast.literal_eval(raw_output)
        return word_list

def cleanup_llm_output_json(raw_output: str) -> str:
        """Clean up LLM output to extract pure JSON"""
        if raw_output.startswith("```json"):
            raw_output = raw_output[len("```json"):].lstrip()
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

def similarity_for_a_field(embeddings_resume,embeddings_job_post, field_name, threshold=0.5):
    matrix = []
    for field_resume in embeddings_resume:
        field_path_resume = field_resume['field_path']
        resume_original_text = field_resume["original_text"]
        if(field_path_resume==field_name):
            embedding_resume_skill = np.array(field_resume['embedding']).reshape(1,-1)
            for field_job_post in embeddings_job_post:
                field_path_job_post = field_job_post['field_path']  
                job_post_original_text = field_job_post["original_text"]
                if(field_path_job_post==field_name):
                    embedding_job_post_hard_skill = np.array(field_job_post['embedding']).reshape(1,-1)
                    similarity_score = cosine_similarity(embedding_resume_skill, embedding_job_post_hard_skill)[0][0]
                    if(similarity_score>=threshold):
                        matrix.append([resume_original_text, job_post_original_text, similarity_score])
                else:
                    pass
        else:
            pass
    return matrix