import requests

def get_similar_words_datamuse(
    term: str,
    topn: int = 50,
    topics: list[str] = None,
    use_synonyms: bool = True,
    use_triggers: bool = False
) -> list[str]:
    """
    Fetch similar words using Datamuse API with optional constraints.
    """
    url = "https://api.datamuse.com/words"
    params = {
        "ml": term,
        "max": topn
    }

    if topics:
        params["topics"] = ",".join(topics)
    
    if use_synonyms:
        params["rel_syn"] = term
    
    if use_triggers:
        params["rel_trg"] = term
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        words = [item["word"] for item in results]
        return list(set(words))  # remove duplicates
    except Exception as e:
        print(f"Error fetching from Datamuse: {e}")
        return []
