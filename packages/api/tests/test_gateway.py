import pytest
from unittest.mock import MagicMock
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.client import GatewayClient
from src.services.gateway.schemas import QuotationDraft, QuotationItem, QuotationStatus


@pytest.fixture
def mock_adapter():
    adapter = MockGatewayAdapter()
    # Speed up tests by reducing latency
    adapter._min_latency = 0.01
    adapter._max_latency = 0.02
    adapter._error_rate = 0.0
    return adapter


@pytest.fixture
def gateway_client(mock_adapter):
    return GatewayClient(mock_adapter)


@pytest.mark.asyncio
async def test_create_draft_success(gateway_client):
    draft = QuotationDraft(
        customer_name="Test Corp",
        items=[QuotationItem(item_code="A1", description="Part A", quantity=10)],
    )
    response = await gateway_client.create_draft(draft)
    assert response.success is True
    assert response.external_id.startswith("LEG-")
    assert response.status == QuotationStatus.DRAFT


@pytest.mark.asyncio
async def test_submit_quotation_success(gateway_client):
    draft = QuotationDraft(customer_name="Test Corp", items=[])
    create_res = await gateway_client.create_draft(draft)

    submit_res = await gateway_client.submit_quotation(create_res.external_id)
    assert submit_res.success is True
    assert submit_res.status == QuotationStatus.SUBMITTED


@pytest.mark.asyncio
async def test_get_status_success(gateway_client):
    draft = QuotationDraft(customer_name="Test Corp", items=[])
    create_res = await gateway_client.create_draft(draft)

    status_info = await gateway_client.get_status(create_res.external_id)
    assert status_info.external_id == create_res.external_id
    assert status_info.status == QuotationStatus.DRAFT


@pytest.mark.asyncio
async def test_mock_adapter_errors(mock_adapter, gateway_client):
    mock_adapter._error_rate = 1.0  # Force errors

    draft = QuotationDraft(customer_name="Test Corp", items=[])
    with pytest.raises(Exception, match="503 Service Unavailable"):
        await gateway_client.create_draft(draft)
