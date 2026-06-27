import pytest
from unittest.mock import AsyncMock, patch
from src.ai.parser import AIQuotationParser
from packages.shared.types.quotation import QuotationDraft, ConfidenceLevel

@pytest.mark.asyncio
async def test_parse_quotation_request():
    parser = AIQuotationParser()

    mock_response = AsyncMock()
    mock_response.choices = [
        AsyncMock(message=AsyncMock(content='{"customer_name": "ACME Corp", "items": [{"material_code": "R10K", "quantity": 100, "confidence": "high", "missing": false}], "confidence_scores": {"customer_name": "high"}}'))
    ]

    with patch("litellm.acompletion", return_value=mock_response):
        result = await parser.parse_quotation_request("Email content", [], "Chat text")

    assert isinstance(result, QuotationDraft)
    assert result.customer_name == "ACME Corp"
    assert len(result.items) == 1
    assert result.items[0].material_code == "R10K"
    assert result.items[0].quantity == 100
    assert result.confidence_scores["customer_name"] == ConfidenceLevel.HIGH

@pytest.mark.asyncio
async def test_parse_quotation_request_invalid_json():
    parser = AIQuotationParser()

    mock_response = AsyncMock()
    mock_response.choices = [
        AsyncMock(message=AsyncMock(content='Invalid JSON'))
    ]

    with patch("litellm.acompletion", return_value=mock_response):
        result = await parser.parse_quotation_request("Email content", [], "Chat text")

    assert isinstance(result, QuotationDraft)
    assert result.customer_name is None
