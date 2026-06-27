from fastapi import APIRouter, HTTPException, Depends
from src.services.gateway.client import GatewayClient
from src.services.gateway.mock_adapter import MockGatewayAdapter
from src.services.gateway.schemas import GatewayResponse, QuotationDraft, QuotationStatus

router = APIRouter(prefix="/api/gateway", tags=["gateway"])

# In a real app, this would be managed via dependency injection and configuration
_mock_adapter = MockGatewayAdapter()
_gateway_client = GatewayClient(_mock_adapter)

def get_gateway_client() -> GatewayClient:
    return _gateway_client

@router.post("/submit/{draft_id}", response_model=GatewayResponse)
async def submit_to_legacy_system(
    draft_id: str,
    client: GatewayClient = Depends(get_gateway_client)
) -> GatewayResponse:
    """
    Trigger the submission of a local draft to the legacy system.
    In this mock implementation, we assume the draft exists locally and
    is pushed to the legacy system as a draft first, then submitted.
    """
    # Mock finding the local draft (in reality, query the DB)
    # For demonstration, we'll create a dummy draft and push it.

    # AC-4: 草稿确认后通过 Gateway 一次性推送到"现有系统"
    dummy_draft = QuotationDraft(
        customer_name="Test Customer",
        items=[],
        total_amount=0.0,
        remarks=f"Local Draft ID: {draft_id}"
    )

    try:
        # 1. Create draft in legacy system
        create_res = await client.create_draft(dummy_draft)
        if not create_res.success or not create_res.external_id:
            raise HTTPException(status_code=500, detail="Failed to create draft in legacy system")

        # 2. Submit it
        submit_res = await client.submit_quotation(create_res.external_id)
        return submit_res
    except Exception as e:
        if "503" in str(e):
             raise HTTPException(status_code=503, detail="Legacy System Unavailable")
        raise HTTPException(status_code=500, detail=str(e))
