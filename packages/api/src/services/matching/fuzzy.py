from rapidfuzz import fuzz

def calculate_similarity(s1: str, s2: str) -> float:
    """
    Calculates the similarity ratio between two strings using rapidfuzz token_sort_ratio.
    Returns a score between 0 and 1.
    """
    if not s1 or not s2:
        return 0.0
    return fuzz.token_sort_ratio(s1, s2) / 100.0
