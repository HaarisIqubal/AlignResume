from src.model.JobPostingSchema import JobPosting

def is_single_word(text: str) -> bool:
    return len(text.strip().split()) == 1 and text.strip().isalpha()

def is_keyword_phrase(text: str) -> bool:
    words = text.strip().split()
    return 2 <= len(words) <= 4 and all(w.isalpha() for w in words)

def is_full_phrase(text: str) -> bool:
    return len(text.strip().split()) > 4 or not text.replace(" ", "").isalpha()

def classify_text_type(text: str) -> str:
    if is_single_word(text):
        return "word"
    elif is_keyword_phrase(text):
        return "word_phrase"
    else:
        return "sentence"

def get_embedding_fields_with_type(job_posting: JobPosting, config: dict) -> dict:
    field_type_map = {}
    for field, use in config.items():
        if not use:
            continue
        value = getattr(job_posting, field, None)

        if not value:
            continue

        # Handle lists
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    text_type = classify_text_type(item)
                    field_type_map.setdefault(field, []).append((item, text_type))

        # Handle strings
        elif isinstance(value, str) and value.strip():
            text_type = classify_text_type(value)
            field_type_map[field] = [(value, text_type)]

    return field_type_map