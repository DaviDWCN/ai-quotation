from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.services.gateway import (
    GatewayClient,
    MockGatewayAdapter,
    GatewayQuotationResponse,
    GatewayQuotationCreate,
)

router = APIRouter()

# Simple dependency injection for the mock client
# In production, this would be configured via settings
_mock_adapter = MockGatewayAdapter()
_gateway_client = GatewayClient(_mock_adapter)

def get_gateway_client() -> GatewayClient:
    return _gateway_client

@router.post("/submit/{draft_id}", response_model=GatewayQuotationResponse)
async def submit_draft(
    draft_id: str,
    client: GatewayClient = Depends(get_gateway_client)
) -> GatewayQuotationResponse:
    """
    Trigger the submission process for a draft.
    AC-4 & AC-6: Draft is pushed to legacy system via Gateway.
    """
    try:
        # In a real scenario, we'd fetch the draft from our local DB first.
        # If it doesn't exist in the legacy system yet, we create it first (AC-4).

        try:
            # Try to submit directly if it already exists in legacy system
            return await client.submit_quotation(draft_id)
        except ValueError:
            # AC-4: If not found in legacy system, we assume it's currently only in our DB
            # and we push it to legacy system now.
            # (In a real app, data would come from local DB, here we mock it)
            new_draft = await client.create_draft(GatewayQuotationCreate(
                customer_id="CUST-AUTO-PUSH",
                items=[]
            ))
            # After creating it in legacy, we submit it.
            return await client.submit_quotation(new_draft.quotation_id)

    except Exception as e:
        if "503" in str(e):
            raise HTTPException(status_code=503, detail="Legacy system temporarily unavailable")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create", response_model=GatewayQuotationResponse)
async def create_quotation(
    data: GatewayQuotationCreate,
    client: GatewayClient = Depends(get_gateway_client)
) -> GatewayQuotationResponse:
    try:
        return await client.create_draft(data)
    except Exception as e:
        if "503" in str(e):
            raise HTTPException(status_code=503, detail="Legacy system temporarily unavailable")
        raise HTTPException(status_code=400, detail=str(e))
