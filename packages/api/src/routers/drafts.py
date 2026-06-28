from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any, Dict
from src.db.session import get_session
from src.services.draft.service import DraftService
from src.db.models import DraftModel
from packages.shared.types.quotation import QuotationDraft, ParsedQuotation
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/drafts", tags=["Drafts"])

class DraftSummary(BaseModel):
    id: str
    customer_id: Optional[str]
    customer_match_score: float
    status: str
    needs_confirmation: bool
    created_at: datetime
    updated_at: datetime

class DraftDetail(DraftSummary):
    customer_candidates: List[Dict[str, Any]]
    parsed_data: Dict[str, Any]
    material_matches: List[Dict[str, Any]]

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
            "created_at": d.created_at,
            "updated_at": d.updated_at
        } for d in drafts
    ]

@router.get("/{draft_id}", response_model=DraftDetail)
async def get_draft(draft_id: str, session: AsyncSession = Depends(get_session)) -> DraftModel:
    service = DraftService(session)
    draft = await service.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft

@router.patch("/{draft_id}", response_model=DraftDetail)
async def update_draft(
    draft_id: str,
    update_data: Dict[str, Any],
    session: AsyncSession = Depends(get_session)
) -> DraftModel:
    service = DraftService(session)
    updated = await service.update_draft(draft_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Draft not found")
    return updated
