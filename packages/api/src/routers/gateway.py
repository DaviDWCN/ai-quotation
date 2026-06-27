from fastapi import APIRouter, HTTPException
from src.services.gateway.client import gateway
from src.services.gateway.schemas import (
    LegacyQuotationResponse,
    LegacyQuotationCreate
)

router = APIRouter(prefix="/gateway", tags=["Gateway"])

@router.post("/submit/{draft_id}", response_model=LegacyQuotationResponse)
async def submit_to_legacy(draft_id: str) -> LegacyQuotationResponse:
    """
    Trigger the submission process for a draft to the legacy system.
    In a real scenario, draft_id refers to our local draft which is then pushed.
    For this mock, we simulate creating a draft in the legacy system and then submitting it.
    """
    try:
        # 1. Simulate fetching local draft data (mocked here)
        # 2. Push to legacy system as a draft
        # 3. Submit the legacy draft

        # Mocking the flow:
        legacy_draft = await gateway.create_draft(
            LegacyQuotationCreate(
                customer_id="CUST-MOCK",
                material_ids=["MAT-1", "MAT-2"],
                external_id=draft_id
            )
        )

        result = await gateway.submit_quotation(legacy_draft.id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quotation/{quotation_id}", response_model=LegacyQuotationResponse)
async def get_legacy_quotation(quotation_id: str) -> LegacyQuotationResponse:
    try:
        return await gateway.get_quotation(quotation_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
