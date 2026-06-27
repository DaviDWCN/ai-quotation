import pytest
from src.services.wecom.card_push import send_approval_card
from src.services.wecom.mock_wecom import MockWeComAdapter
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_approval_card():
    mock_adapter = MockWeComAdapter()
    mock_adapter.send_approval_card = AsyncMock()

    await send_approval_card(
        adapter=mock_adapter,
        user_id="user123",
        draft_id="draft456",
        customer_name="Test Customer",
        material_summary="Test Material Summary"
    )

    mock_adapter.send_approval_card.assert_called_once_with(
        user_id="user123",
        draft_id="draft456",
        customer_name="Test Customer",
        material_summary="Test Material Summary",
        jump_url="http://localhost:3000/quotation/draft/draft456"
    )
