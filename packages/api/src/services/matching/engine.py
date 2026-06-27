from typing import List, Tuple, Optional, Any
from .fuzzy import calculate_similarity
from shared.types.master_data import Customer, Material

class MatchingEngine:
    def __init__(self, customers: List[Customer], materials: List[Material]):
        self.customers = customers
        self.materials = materials

    def match_customer(self, name: str, top_n: int = 3) -> List[Tuple[Customer, float]]:
        results = []
        for customer in self.customers:
            score = calculate_similarity(name, customer.name)
            results.append((customer, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]

    def match_material(self, name: str, top_n: int = 3) -> List[Tuple[Material, float]]:
        results = []
        for material in self.materials:
            # Match against name or code if available
            name_score = calculate_similarity(name, material.name)
            code_score = calculate_similarity(name, material.code) if material.code else 0.0
            score = max(name_score, code_score)
            results.append((material, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
