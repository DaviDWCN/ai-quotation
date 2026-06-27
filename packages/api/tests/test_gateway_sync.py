import pytest
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.client import IntegrationGateway
from src.services.gateway.sync_service import StatusSyncService
from src.services.gateway.schemas import LegacyQuotationCreate

@pytest.fixture
def mock_adapter():
    adapter = MockGatewayAdapter()
    async def fast_simulate():
        pass
    adapter._simulate_behavior = fast_simulate
    return adapter

@pytest.fixture
def sync_service(mock_adapter):
    service = StatusSyncService()
    # Inject mock gateway client with our fast adapter
    service.gateway = IntegrationGateway(adapter=mock_adapter)
    return service

@pytest.mark.asyncio
async def test_sync_all_pending(sync_service):
    # 1. Create and submit some quotations in the mock system
    gateway = sync_service.gateway

    q1 = await gateway.create_draft(LegacyQuotationCreate(customer_id="C1", material_ids=["M1"]))
    await gateway.submit_quotation(q1.id)

    q2 = await gateway.create_draft(LegacyQuotationCreate(customer_id="C2", material_ids=["M2"]))
    # q2 stays as DRAFT

    q3 = await gateway.create_draft(LegacyQuotationCreate(customer_id="C3", material_ids=["M3"]))
    await gateway.submit_quotation(q3.id)

    # 2. Run sync
    synced = await sync_service.sync_all_pending()

    # 3. Verify
    assert len(synced) == 2
    ids = [q.id for q in synced]
    assert q1.id in ids
    assert q3.id in ids
    assert q2.id not in ids
