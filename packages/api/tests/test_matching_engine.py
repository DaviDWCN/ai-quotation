import pytest
import os
from src.services.matching.engine import MatchingEngine

@pytest.fixture
def matching_engine():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_master_data.json")
    return MatchingEngine(fixture_path)

def test_match_customer_exact(matching_engine):
    best_id, score, candidates = matching_engine.match_customer("TechCorp Solutions")
    assert best_id == "C001"
    assert score == 1.0

def test_match_customer_fuzzy(matching_engine):
    # Slight variation in name
    best_id, score, candidates = matching_engine.match_customer("Tech Corp Solution")
    assert best_id == "C001"
    assert score > 0.9

def test_match_customer_low_score(matching_engine):
    best_id, score, candidates = matching_engine.match_customer("Completely Unknown Inc")
    assert best_id is None
    assert score < 0.85

def test_match_material_code(matching_engine):
    best_id, score, candidates = matching_engine.match_material("SP-010")
    assert best_id == "M001"
    assert score == 1.0

def test_match_material_name_fuzzy(matching_engine):
    best_id, score, candidates = matching_engine.match_material("Steel Plt 10mm")
    assert best_id == "M001"
    assert score > 0.85
