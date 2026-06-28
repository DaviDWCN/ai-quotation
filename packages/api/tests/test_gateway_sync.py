import pytest
import asyncio
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.client import GatewayClient
from src.services.gateway.sync_service import SyncService
from src.services.gateway.schemas import GatewayQuotationCreate, GatewayQuotationStatus

@pytest.fixture
def mock_adapter():
    return MockGatewayAdapter(enable_errors=False, enable_delay=False)

@pytest.fixture
def gateway_client(mock_adapter):
    return GatewayClient(mock_adapter)

@pytest.fixture
def sync_service(gateway_client):
    return SyncService(gateway_client)

@pytest.mark.asyncio
async def test_sync_quotation_statuses(sync_service, gateway_client):
    # Create a few drafts
    draft1 = await gateway_client.create_draft(GatewayQuotationCreate(customer_id="C1", items=[]))
    draft2 = await gateway_client.create_draft(GatewayQuotationCreate(customer_id="C2", items=[]))

    # Submit one
    await gateway_client.submit_quotation(draft1.quotation_id)

    # Sync
    await sync_service.sync_quotation_statuses([draft1.quotation_id, draft2.quotation_id])

    # Verify we can still get statuses
    status1 = await gateway_client.get_status(draft1.quotation_id)
    status2 = await gateway_client.get_status(draft2.quotation_id)

    assert status1.status in [
        GatewayQuotationStatus.SUBMITTED,
        GatewayQuotationStatus.APPROVED,
        GatewayQuotationStatus.REJECTED
    ]
    assert status2.status == GatewayQuotationStatus.DRAFT
