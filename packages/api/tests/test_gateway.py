import pytest
import asyncio
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.client import GatewayClient
from src.services.gateway.schemas import (
    GatewayQuotationCreate,
    GatewayQuotationItem,
    GatewayQuotationStatus,
    GatewayQuotationUpdate
)

@pytest.fixture
def mock_adapter():
    # Disable errors and delay for stable tests
    return MockGatewayAdapter(enable_errors=False, enable_delay=False)

@pytest.fixture
def gateway_client(mock_adapter):
    return GatewayClient(mock_adapter)

@pytest.mark.asyncio
async def test_create_draft(gateway_client):
    data = GatewayQuotationCreate(
        customer_id="CUST-001",
        items=[GatewayQuotationItem(material_id="MAT-001", quantity=10.0)]
    )
    response = await gateway_client.create_draft(data)
    assert response.quotation_id is not None
    assert response.customer_id == "CUST-001"
    assert response.status == GatewayQuotationStatus.DRAFT
    assert len(response.items) == 1

@pytest.mark.asyncio
async def test_submit_quotation(gateway_client):
    # Create draft
    data = GatewayQuotationCreate(customer_id="CUST-001", items=[])
    draft = await gateway_client.create_draft(data)

    # Submit draft
    submitted = await gateway_client.submit_quotation(draft.quotation_id)
    assert submitted.status == GatewayQuotationStatus.SUBMITTED
    assert submitted.quotation_id == draft.quotation_id

@pytest.mark.asyncio
async def test_update_quotation(gateway_client):
    # Create draft
    data = GatewayQuotationCreate(customer_id="CUST-001", items=[])
    draft = await gateway_client.create_draft(data)

    # Update draft
    update_data = GatewayQuotationUpdate(
        items=[GatewayQuotationItem(material_id="MAT-002", quantity=5.0, price=100.0)]
    )
    updated = await gateway_client.update_quotation(draft.quotation_id, update_data)
    assert len(updated.items) == 1
    assert updated.items[0].material_id == "MAT-002"

@pytest.mark.asyncio
async def test_get_status(gateway_client):
    data = GatewayQuotationCreate(customer_id="CUST-001", items=[])
    draft = await gateway_client.create_draft(data)

    status_resp = await gateway_client.get_status(draft.quotation_id)
    assert status_resp.quotation_id == draft.quotation_id
    assert status_resp.status == GatewayQuotationStatus.DRAFT

@pytest.mark.asyncio
async def test_mock_error_handling():
    # Enable errors to test the 5% failure rate
    err_adapter = MockGatewayAdapter(enable_errors=True, enable_delay=False)
    err_client = GatewayClient(err_adapter)

    errors_caught = 0
    # Try multiple times to hit the 5% error
    for _ in range(200):
        try:
            await err_client.get_status("some-id")
        except ValueError:
            # Expected if ID not found and no 503
            pass
        except Exception as e:
            if "503" in str(e):
                errors_caught += 1
                break

    assert errors_caught > 0, "Should have caught at least one 503 error in 200 attempts"
