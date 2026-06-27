import pytest
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.client import GatewayClient
from src.services.gateway.sync_service import GatewaySyncService
from src.services.gateway.schemas import QuotationDraft


@pytest.fixture
def gateway_client():
    adapter = MockGatewayAdapter()
    adapter._min_latency = 0.01
    adapter._max_latency = 0.02
    adapter._error_rate = 0.0
    return GatewayClient(adapter)


@pytest.fixture
def sync_service(gateway_client):
    return GatewaySyncService(gateway_client)


@pytest.mark.asyncio
async def test_sync_quotation_statuses(sync_service, gateway_client):
    # Setup: create some drafts
    draft = QuotationDraft(customer_name="Sync Test", items=[])
    res1 = await gateway_client.create_draft(draft)
    res2 = await gateway_client.create_draft(draft)

    external_ids = [res1.external_id, res2.external_id]

    # Run sync
    await sync_service.sync_quotation_statuses(external_ids)

    # Verification is mostly via logging in this mock,
    # but we ensure it doesn't raise exceptions.
    assert True
