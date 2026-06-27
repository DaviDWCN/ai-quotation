import pytest
from src.services.matching.engine import MatchingEngine
from shared.types.master_data import Customer, Material

def test_match_customer():
    customers = [
        Customer(id="1", name="Apple Inc"),
        Customer(id="2", name="Microsoft Corp"),
    ]
    engine = MatchingEngine(customers, [])

    # Exact match
    matches = engine.match_customer("Apple Inc")
    assert matches[0][0].id == "1"
    assert matches[0][1] == 1.0

    # Fuzzy match
    matches = engine.match_customer("Apple")
    assert matches[0][0].id == "1"
    assert matches[0][1] > 0.7

    # Low score match
    matches = engine.match_customer("Google")
    assert matches[0][1] < 0.5

def test_match_material():
    materials = [
        Material(id="m1", name="Screw M8", unit_price=1.0, code="S8"),
        Material(id="m2", name="Bolt M10", unit_price=2.0, code="B10"),
    ]
    engine = MatchingEngine([], materials)

    matches = engine.match_material("Screw")
    assert matches[0][0].id == "m1"

    # Match by code
    matches = engine.match_material("B10")
    assert matches[0][0].id == "m2"
    assert matches[0][1] == 1.0
