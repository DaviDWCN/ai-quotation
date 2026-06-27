import pytest
from fastapi import HTTPException
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.client import IntegrationGateway
from src.services.gateway.schemas import (
    LegacyQuotationCreate,
    LegacyQuotationUpdate,
    LegacyQuotationStatus
)

@pytest.fixture
def mock_adapter():
    # Disable simulation for faster/reliable tests
    adapter = MockGatewayAdapter()
    async def fast_simulate():
        pass
    adapter._simulate_behavior = fast_simulate
    return adapter

@pytest.fixture
def gateway(mock_adapter):
    return IntegrationGateway(adapter=mock_adapter)

@pytest.mark.asyncio
async def test_create_draft(gateway):
    draft_data = LegacyQuotationCreate(
        customer_id="CUST001",
        material_ids=["MAT001", "MAT002"]
    )
    response = await gateway.create_draft(draft_data)

    assert response.id.startswith("LEG-")
    assert response.customer_id == "CUST001"
    assert response.status == LegacyQuotationStatus.DRAFT

@pytest.mark.asyncio
async def test_submit_quotation(gateway):
    # First create
    draft_data = LegacyQuotationCreate(
        customer_id="CUST001",
        material_ids=["MAT001"]
    )
    draft = await gateway.create_draft(draft_data)

    # Then submit
    submitted = await gateway.submit_quotation(draft.id)
    assert submitted.id == draft.id
    assert submitted.status == LegacyQuotationStatus.SUBMITTED

@pytest.mark.asyncio
async def test_update_quotation(gateway):
    draft_data = LegacyQuotationCreate(
        customer_id="CUST001",
        material_ids=["MAT001"]
    )
    draft = await gateway.create_draft(draft_data)

    update_data = LegacyQuotationUpdate(
        material_ids=["MAT001", "MAT002"]
    )
    updated = await gateway.update_quotation(draft.id, update_data)
    assert updated.material_ids == ["MAT001", "MAT002"]

@pytest.mark.asyncio
async def test_get_quotation_not_found(gateway):
    with pytest.raises(HTTPException) as excinfo:
        await gateway.get_quotation("NON-EXISTENT")
    assert excinfo.value.status_code == 404
