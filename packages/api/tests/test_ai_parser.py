import pytest
from unittest.mock import AsyncMock, patch
from src.ai.parser import parse_quotation_request, convert_to_quotation_draft
from src.ai.schemas import ExtractedQuotation
from src.ai.confidence import ConfidenceLevel

@pytest.fixture
def mock_extracted_data():
    return {
        "customer_name": {"value": "ABC Corp", "confidence": "high", "missing": False},
        "segmentation": {"value": "Industrial", "confidence": "medium", "missing": False},
        "items": [
            {
                "material_code": {"value": "MOD-123", "confidence": "high", "missing": False},
                "quantity": {"value": 100.0, "confidence": "high", "missing": False},
                "target_price": {"value": 50.5, "confidence": "medium", "missing": False},
                "unit": {"value": "pcs", "confidence": "high", "missing": False},
                "remarks": {"value": None, "confidence": "low", "missing": True}
            }
        ],
        "delivery_date": {"value": "2023-12-31", "confidence": "high", "missing": False},
        "remarks": {"value": "Urgent", "confidence": "medium", "missing": False}
    }

@pytest.mark.asyncio
@patch("src.ai.parser.acompletion")
@patch("src.ai.parser.extract_documents_text")
async def test_parse_quotation_request(mock_extract, mock_acompletion, mock_extracted_data):
    # Mock Document Extraction
    mock_extract.return_value = "Mocked PDF Content"

    # Mock LLM response
    mock_response = AsyncMock()
    mock_response.choices = [
        AsyncMock(message=AsyncMock(content='{"customer_name": {"value": "ABC Corp", "confidence": "high", "missing": false}, "segmentation": {"value": "Industrial", "confidence": "medium", "missing": false}, "items": [{"material_code": {"value": "MOD-123", "confidence": "high", "missing": false}, "quantity": {"value": 100.0, "confidence": "high", "missing": false}, "target_price": {"value": 50.5, "confidence": "medium", "missing": false}, "unit": {"value": "pcs", "confidence": "high", "missing": false}, "remarks": {"value": null, "confidence": "low", "missing": true}}], "delivery_date": {"value": "2023-12-31", "confidence": "high", "missing": false}, "remarks": {"value": "Urgent", "confidence": "medium", "missing": false}}'))
    ]
    mock_acompletion.return_value = mock_response

    email_content = "Please quote for ABC Corp"
    attachments = [(b"Dummy PDF", "test.pdf")]

    result = await parse_quotation_request(email_content, attachments)

    assert isinstance(result, ExtractedQuotation)
    assert result.customer_name.value == "ABC Corp"
    assert len(result.items) == 1
    assert result.items[0].material_code.value == "MOD-123"

def test_convert_to_quotation_draft(mock_extracted_data):
    extracted = ExtractedQuotation.model_validate(mock_extracted_data)
    draft = convert_to_quotation_draft(extracted, "draft-123")

    assert draft.id == "draft-123"
    assert draft.parsed_data.customer_name == "ABC Corp"
    assert len(draft.parsed_data.items) == 1
    assert draft.parsed_data.items[0].code == "MOD-123"
    assert draft.parsed_data.items[0].quantity == 100.0
    assert draft.parsed_data.metadata["segmentation"] == "Industrial"
