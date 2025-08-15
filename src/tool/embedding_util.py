from src.model.JobPostingSchema import JobPosting
from src.tool.llm_manager import llm_manager
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import PromptTemplate
import ast
from typing import List, Tuple, Any,Iterable, Sequence
import re
import json



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

# def get_similar_terms_from_llm(term: str, api_key: str) -> list[str]:
#     prompt = PromptTemplate(
#     template="""You are a helpful assistant. For the term '{term}', generate a list of 5 closely related words or short phrases. These should capture synonyms, related job titles, and conceptually similar terms. Avoid full sentences. Keep short phrases. Make sure you do not leave anything empty. Only return a Python list of strings.""",
#         input_variables=["term"]
#     )
    
#     parser = StrOutputParser()
#     chain = llm_manager.init_llm_chain(prompt=prompt)
#     try:
#         sim_word_list = chain.invoke({"term": term})
#         return sim_word_list
#     except Exception as e:
#         print(f"Exception {e}")
#         return 
#     finally:
#         print("Finally passed")


def transform_input_to_output_with_llm(
    input_format: Iterable[Sequence[str]],   # supports list of tuples or lists
    similar_k: int = 10
) -> List[List[Any]]:
    """
    Transform [(key, value), ...] (or [[key, value], ...]) into
    [[key, [value, sim1..simK]], ...] using a single LLM call with strict JSON output.

    Args:
        input_format: Iterable of 2-item sequences (tuples or lists) of strings.
        api_key:      API key for the underlying LLM (used by llm_manager).
        similar_k:    Number of similar terms to include (default 10).
        max_tokens:   Model output cap (passed via llm_manager if supported).
        temperature:  Sampling temperature.

    Returns:
        output_format: [[key, [value, sim1..simK]], ...]
    """

    # --- Normalize and validate input: accept tuples/lists, enforce len=2 and str types ---
    normalized: List[List[str]] = []
    for idx, pair in enumerate(input_format):
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            raise ValueError(f"Item {idx} must be a 2-item tuple/list. Got: {pair!r}")
        key, value = pair[0], pair[1]
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError(f"Both key and value must be strings at index {idx}. Got: {pair!r}")
        normalized.append([key, value])

    # --- Prompt with strict JSON contract ---
    template = f"""
You are a meticulous data wrangler. Your job is to transform an input list of [key, value] pairs into an output list where each item is:
[key, [value, similar_1, similar_2, ..., similar_{similar_k}]]

"Similar words" means concise synonyms or closely related terms for the entire value phrase (domain-relevant skills, functions, tools, or concepts). Optimize for usefulness in search/matching.

STRICT RULES:
1) Output MUST be valid, minified JSON only. No comments, no prose, no code fences.
2) For every item: the second element is a list of EXACTLY {similar_k + 1} strings:
   - the original value as the first element,
   - followed by {similar_k} distinct, high-quality similar terms.
3) Terms: keep each ≤3 words; avoid duplicates; avoid acronyms-only entries unless widely recognized.
4) Use American English; Title Case only for proper nouns; otherwise sentence case is fine.
5) If a value has multiple themes, distribute the similar terms across those themes.
6) No filler words (e.g., "etc."), no meaningless numbers. Include standards (e.g., "ISO 31000") only if clearly relevant.
7) Preserve the original value text verbatim as the first element.

Return JSON ONLY in this exact structure:
[
  [key1, [value1, sim1, sim2, ..., sim{similar_k}]],
  [key2, [value2, sim1, sim2, ..., sim{similar_k}]],
  ...
]

Here is input_format:
{{input_json}}
""".strip()

    prompt = PromptTemplate(template=template, input_variables=["input_json"])
    parser = StrOutputParser()

    chain = llm_manager.init_llm_chain(
        prompt=prompt
    )

    try:
        input_json = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))
        raw = chain.invoke({"input_json": input_json})

        # Strip optional code fences just in case
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE | re.DOTALL).strip()

        data = json.loads(cleaned)

        # Validate structure and lengths
        def is_str_list(x):
            return isinstance(x, list) and all(isinstance(i, str) for i in x)

        output: List[List[Any]] = []
        for idx, item in enumerate(data):
            if not (isinstance(item, list) and len(item) == 2):
                raise ValueError(f"Item {idx} is not [key, list]. Got: {item!r}")
            key, val_list = item[0], item[1]
            if not isinstance(key, str) or not is_str_list(val_list):
                raise ValueError(f"Invalid types at index {idx}. Got: {item!r}")

            # Enforce exact length (value + similar_k)
            needed = similar_k + 1
            if len(val_list) < needed:
                last = val_list[-1] if val_list else ""
                val_list = val_list + [last] * (needed - len(val_list))
            elif len(val_list) > needed:
                val_list = val_list[:needed]

            output.append([key, val_list])

        return output

    except json.JSONDecodeError as e:
        print("Failed to parse LLM JSON. Raw output was:\n", raw)
        raise e
    except Exception as e:
        print(f"Exception: {e}")
        raise
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