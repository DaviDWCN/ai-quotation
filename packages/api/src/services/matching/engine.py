import json
from typing import List, Dict, Any, Optional, Tuple
from .fuzzy import find_best_matches, get_similarity_score

class MatchingEngine:
    def __init__(self, master_data_path: str):
        with open(master_data_path, 'r') as f:
            self.master_data = json.load(f)

        self.customers = self.master_data.get("customers", [])
        self.materials = self.master_data.get("materials", [])

        self.customer_names = [c["name"] for c in self.customers]
        self.material_names = [m["name"] for m in self.materials]
        self.material_codes = [m["code"] for m in self.materials if m.get("code")]

    def match_customer(self, name: str, threshold: float = 0.85) -> Tuple[Optional[str], float, List[Dict[str, Any]]]:
        """Match a customer name against master data."""
        if not name:
            return None, 0.0, []

        matches = find_best_matches(name, self.customer_names)
        candidates = []
        best_id = None
        best_score = 0.0

        for matched_name, score in matches:
            customer = next(c for c in self.customers if c["name"] == matched_name)
            candidates.append({**customer, "match_score": score})
            if score > best_score:
                best_score = score
                best_id = customer["id"]

        if best_score < threshold:
            best_id = None # Marks as needs_confirmation if below threshold

        return best_id, best_score, candidates

    def match_material(self, name_or_code: str, threshold: float = 0.85) -> Tuple[Optional[str], float, List[Dict[str, Any]]]:
        """Match a material name or code against master data."""
        if not name_or_code:
            return None, 0.0, []

        # Try exact code match first
        for material in self.materials:
            if material.get("code") == name_or_code:
                return material["id"], 1.0, [{**material, "match_score": 1.0}]

        # Try fuzzy match on name
        name_matches = find_best_matches(name_or_code, self.material_names)

        # Also try fuzzy match on code
        code_matches = find_best_matches(name_or_code, self.material_codes)

        all_matches = []
        seen_ids = set()

        for matched_name, score in name_matches:
            material = next(m for m in self.materials if m["name"] == matched_name)
            if material["id"] not in seen_ids:
                all_matches.append({**material, "match_score": score})
                seen_ids.add(material["id"])

        for matched_code, score in code_matches:
            material = next(m for m in self.materials if m.get("code") == matched_code)
            if material["id"] not in seen_ids:
                all_matches.append({**material, "match_score": score})
                seen_ids.add(material["id"])
            else:
                # Update score if code match is better
                for m in all_matches:
                    if m["id"] == material["id"]:
                        m["match_score"] = max(m["match_score"], score)

        # Sort by score
        all_matches.sort(key=lambda x: x["match_score"], reverse=True)
        candidates = all_matches[:5]

        best_id = None
        best_score = 0.0
        if candidates:
            best_score = candidates[0]["match_score"]
            if best_score >= threshold:
                best_id = candidates[0]["id"]

        return best_id, best_score, candidates
