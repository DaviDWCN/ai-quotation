import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.draft.service import DraftService
from src.services.matching.engine import MatchingEngine
from src.services.notification.service import NotificationService
from shared.types.master_data import Customer, Material
from shared.types.quotation import QuotationStatus

@pytest.mark.asyncio
async def test_create_draft_from_ai_result():
    db = AsyncMock()
    matching_engine = MagicMock(spec=MatchingEngine)
    notification_service = AsyncMock(spec=NotificationService)

    # Mock data
    customer = Customer(id="c1", name="Test Customer")
    material = Material(id="m1", name="Test Material", unit_price=10.0)

    matching_engine.match_customer.return_value = [(customer, 0.9)]
    matching_engine.match_material.return_value = [(material, 0.9)]

    service = DraftService(db, matching_engine, notification_service)

    ai_data = {
        "customer_name": "Test Cust",
        "items": [
            {"name": "Test Mat", "quantity": 5}
        ]
    }

    draft = await service.create_draft_from_ai_result(ai_data)

    assert draft.customer_name_raw == "Test Cust"
    assert draft.matched_customer_id == "c1"
    assert len(draft.items) == 1
    assert draft.items[0].matched_material_id == "m1"
    assert draft.needs_confirmation is False

    db.add.assert_called_once()
    db.commit.assert_called_once()
    notification_service.send_draft_notification.assert_called_once()

@pytest.mark.asyncio
async def test_create_draft_needs_confirmation():
    db = AsyncMock()
    matching_engine = MagicMock(spec=MatchingEngine)
    notification_service = AsyncMock(spec=NotificationService)

    matching_engine.match_customer.return_value = [(Customer(id="c1", name="C"), 0.5)]
    matching_engine.match_material.return_value = [(Material(id="m1", name="M", unit_price=1.0), 0.5)]

    service = DraftService(db, matching_engine, notification_service)

    ai_data = {
        "customer_name": "Unknown",
        "items": [{"name": "Unknown Mat"}]
    }

    draft = await service.create_draft_from_ai_result(ai_data)

    assert draft.matched_customer_id is None
    assert draft.needs_confirmation is True
    assert draft.items[0].matched_material_id is None
