import pytest
from unittest.mock import AsyncMock, patch
from src.ai.parser import parse_quotation_request
from src.ai.schemas import AIParserOutput, ConfidenceLevel
from packages.shared.types.quotation import QuotationDraft

@pytest.mark.asyncio
async def test_parse_quotation_request_success():
    # Mock litellm.acompletion
    mock_response = AsyncMock()
    mock_response.choices = [
        AsyncMock(message=AsyncMock(content='''
        {
          "customer_name": {"value": "Acme Corp", "confidence": "high", "missing": false},
          "segmentation": {"value": "Solar", "confidence": "high", "missing": false},
          "items": [
            {
              "material_code": {"value": "SP-500", "confidence": "high", "missing": false},
              "quantity": {"value": 20, "confidence": "high", "missing": false},
              "unit": {"value": "pcs", "confidence": "high", "missing": false},
              "target_price": {"value": 200, "confidence": "high", "missing": false}
            }
          ],
          "delivery_date": {"value": "2024-07-01", "confidence": "medium", "missing": false},
          "remarks": {"value": "Urgent", "confidence": "high", "missing": false}
        }
        '''))
    ]

    with patch("litellm.acompletion", return_value=mock_response):
        result = await parse_quotation_request(chat_text="Test chat")

        assert isinstance(result, QuotationDraft)
        assert result.customer_name == "Acme Corp"
        assert result.segmentation == "Solar"
        assert len(result.items) == 1
        assert result.items[0].material_code == "SP-500"
        assert result.items[0].quantity == 20

@pytest.mark.asyncio
async def test_parse_quotation_request_retry():
    # Mock litellm.acompletion to fail once then succeed
    mock_response_success = AsyncMock()
    mock_response_success.choices = [
        AsyncMock(message=AsyncMock(content='''
        {
          "customer_name": {"value": "Acme Corp", "confidence": "high", "missing": false},
          "segmentation": {"value": null, "confidence": "low", "missing": true},
          "items": [],
          "delivery_date": {"value": null, "confidence": "low", "missing": true},
          "remarks": {"value": null, "confidence": "low", "missing": true}
        }
        '''))
    ]

    with patch("litellm.acompletion") as mock_completion:
        mock_completion.side_effect = [
            ValueError("LLM Error"), # First attempt fails
            mock_response_success   # Second attempt succeeds
        ]

        result = await parse_quotation_request(chat_text="Test chat", max_retries=1)
        assert result.customer_name == "Acme Corp"
        assert mock_completion.call_count == 2
