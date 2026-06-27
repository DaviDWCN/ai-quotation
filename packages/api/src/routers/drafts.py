from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from src.db.session import get_db
from src.db.models import Draft
from shared.types.quotation import QuotationDraft, QuotationStatus, QuotationItem

router = APIRouter(prefix="/api/drafts", tags=["drafts"])

@router.get("/", response_model=List[dict])
async def list_drafts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Draft))
    drafts = result.scalars().all()
    return [
        {
            "id": d.id,
            "customer_name_raw": d.customer_name_raw,
            "status": d.status,
            "matching_score": d.matching_score,
            "needs_confirmation": d.needs_confirmation
        } for d in drafts
    ]

@router.get("/{draft_id}", response_model=QuotationDraft)
async def get_draft(draft_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Draft)
        .where(Draft.id == draft_id)
        .options(selectinload(Draft.items))
    )
    draft = result.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    return QuotationDraft(
        id=draft.id,
        customer_name_raw=draft.customer_name_raw,
        matched_customer_id=draft.matched_customer_id,
        items=[
            QuotationItem(
                material_name_raw=item.material_name_raw,
                matched_material_id=item.matched_material_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                matching_score=item.matching_score
            ) for item in draft.items
        ],
        status=draft.status,
        matching_score=draft.matching_score,
        needs_confirmation=draft.needs_confirmation,
        raw_data=draft.raw_data,
        created_at=draft.created_at,
        updated_at=draft.updated_at
    )

@router.patch("/{draft_id}")
async def update_draft(draft_id: str, updates: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Draft).where(Draft.id == draft_id))
    draft = result.scalar_one_or_none()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    if "status" in updates:
        draft.status = QuotationStatus(updates["status"])
    if "matched_customer_id" in updates:
        draft.matched_customer_id = updates["matched_customer_id"]

    await db.commit()
    return {"message": "Draft updated"}
