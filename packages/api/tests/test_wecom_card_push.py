import pytest
from src.services.wecom.card_push import send_approval_card
from src.services.wecom.mock_wecom import MockWeComAdapter


@pytest.mark.asyncio
async def test_send_approval_card() -> None:
    adapter = MockWeComAdapter()
    user_id = "user123"
    draft_id = "DRAFT001"
    customer_name = "Test Customer"
    material_summary = "10x Steel Rods"

    result = await send_approval_card(
        adapter, user_id, draft_id, customer_name, material_summary
    )

    assert result["errcode"] == 0
    assert result["errmsg"] == "ok"
    assert result["msgid"] == "mock_msgid"
