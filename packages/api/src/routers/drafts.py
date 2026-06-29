from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict, Literal
from src.db.session import get_session
from src.services.draft.service import DraftService
from packages.shared.types.quotation import QuotationDraft, ParsedQuotation
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/drafts", tags=["Drafts"])

class DraftField(BaseModel):
    value: Optional[Any] = None
    confidence: Literal["high", "medium", "low"]
    required: bool
    label: str

class DraftSummary(BaseModel):
    id: str
    customer_id: Optional[str] = None
    customer_match_score: float = 0.0
    status: str
    needs_confirmation: bool
    fields: Dict[str, DraftField]
    parsed_data: Dict[str, Any]
    material_matches: List[Dict[str, Any]]
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class DraftDetail(DraftSummary):
    customer_candidates: List[Dict[str, Any]]

def map_confidence(score: float) -> Literal["high", "medium", "low"]:
    if score >= 0.9:
        return "high"
    elif score >= 0.6:
        return "medium"
    else:
        return "low"

def assemble_fields(draft: Any) -> Dict[str, DraftField]:
    parsed_data = draft.parsed_data if hasattr(draft, 'parsed_data') else draft.get('parsed_data', {})
    metadata = parsed_data.get('metadata', {})

    # Use field-specific confidence if available, else fallback to global confidence
    global_conf = parsed_data.get('confidence', 0.0)

    customer_name_conf = global_conf
    # items[0] in ParsedQuotation doesn't help with customer name,
    # but ParsedQuotation only has a global confidence currently.

    return {
        "customer_name": DraftField(
            value=parsed_data.get("customer_name"),
            confidence=map_confidence(customer_name_conf),
            required=True,
            label="Customer Name"
        ),
        "date": DraftField(
            value=parsed_data.get("date"),
            confidence=map_confidence(global_conf),
            required=False,
            label="Date"
        ),
        "segmentation": DraftField(
            value=metadata.get("segmentation"),
            confidence=map_confidence(global_conf),
            required=False,
            label="Segmentation"
        ),
        "remarks": DraftField(
            value=metadata.get("remarks"),
            confidence=map_confidence(global_conf),
            required=False,
            label="Remarks"
        )
    }

@router.get("", response_model=List[DraftSummary])
async def list_drafts(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
) -> List[Dict[str, Any]]:
    service = DraftService(session)
    drafts = await service.list_drafts(limit=limit, offset=offset)
    return [
        {
            "id": d.id,
            "customer_id": d.customer_id,
            "customer_match_score": d.customer_match_score,
            "status": d.status,
            "needs_confirmation": d.needs_confirmation,
            "fields": assemble_fields(d),
            "parsed_data": d.parsed_data,
            "material_matches": d.material_matches,
            "file_url": d.parsed_data.get("metadata", {}).get("file_url"),
            "file_type": d.parsed_data.get("metadata", {}).get("file_type"),
            "created_at": d.created_at,
            "updated_at": d.updated_at
        } for d in drafts
    ]

@router.get("/{draft_id}", response_model=DraftDetail)
async def get_draft(draft_id: str, session: AsyncSession = Depends(get_session)) -> Any:
    service = DraftService(session)
    draft = await service.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    res = {
        "id": draft.id,
        "customer_id": draft.customer_id,
        "customer_match_score": draft.customer_match_score,
        "status": draft.status,
        "needs_confirmation": draft.needs_confirmation,
        "fields": assemble_fields(draft),
        "parsed_data": draft.parsed_data,
        "material_matches": draft.material_matches,
        "file_url": draft.parsed_data.get("metadata", {}).get("file_url"),
        "file_type": draft.parsed_data.get("metadata", {}).get("file_type"),
        "created_at": draft.created_at,
        "updated_at": draft.updated_at,
        "customer_candidates": draft.customer_candidates,
    }
    return res

@router.patch("/{draft_id}", response_model=DraftDetail)
async def update_draft(
    draft_id: str,
    update_data: Dict[str, Any],
    session: AsyncSession = Depends(get_session)
) -> Any:
    service = DraftService(session)
    draft = await service.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    if "fields" in update_data:
        fields = update_data.pop("fields")
        parsed_data = draft.parsed_data.copy()
        if "customer_name" in fields:
            parsed_data["customer_name"] = fields["customer_name"].get("value")
        if "date" in fields:
            parsed_data["date"] = fields["date"].get("value")
        if "segmentation" in fields:
            if "metadata" not in parsed_data:
                parsed_data["metadata"] = {}
            parsed_data["metadata"]["segmentation"] = fields["segmentation"].get("value")
        update_data["parsed_data"] = parsed_data

    updated = await service.update_draft(draft_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Draft not found")

    res = {
        "id": updated.id,
        "customer_id": updated.customer_id,
        "customer_match_score": updated.customer_match_score,
        "status": updated.status,
        "needs_confirmation": updated.needs_confirmation,
        "fields": assemble_fields(updated),
        "parsed_data": updated.parsed_data,
        "material_matches": updated.material_matches,
        "file_url": updated.parsed_data.get("metadata", {}).get("file_url"),
        "file_type": updated.parsed_data.get("metadata", {}).get("file_type"),
        "created_at": updated.created_at,
        "updated_at": updated.updated_at,
        "customer_candidates": updated.customer_candidates,
    }
    return res
