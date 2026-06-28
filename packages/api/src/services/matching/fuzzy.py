from rapidfuzz import fuzz, process
from typing import List, Tuple, Any

def get_similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity score between two strings using rapidfuzz."""
    if not s1 or not s2:
        return 0.0
    # WRatio is generally better for shorter strings and accounts for case/punctuation
    score: float = fuzz.WRatio(s1, s2)
    return score / 100.0

def find_best_matches(query: str, choices: List[str], limit: int = 5) -> List[Tuple[str, float]]:
    """Find the best matching strings from a list of choices."""
    if not query or not choices:
        return []

    results = process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        limit=limit
    )

    return [(choice, score / 100.0) for choice, score, _ in results]
