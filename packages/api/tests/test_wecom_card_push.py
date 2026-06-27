import pytest
from src.services.wecom.card_push import CardPushService
from src.services.wecom.mock_wecom import MockWeComAdapter

@pytest.mark.asyncio
async def test_send_approval_card():
    wecom_adapter = MockWeComAdapter()
    card_service = CardPushService(wecom_adapter)

    await card_service.send_approval_card(
        user_id="user123",
        draft_id="DRAFT001",
        customer_name="Test Customer",
        material_summary="Material A, Material B"
    )

    assert len(wecom_adapter.sent_messages) == 1
    msg = wecom_adapter.sent_messages[0]
    assert msg["type"] == "template_card"
    assert msg["user_id"] == "user123"
    assert msg["card_data"]["main_title"]["desc"] == "草稿单号: DRAFT001"
    assert msg["card_data"]["horizontal_content_list"][0]["value"] == "Test Customer"
