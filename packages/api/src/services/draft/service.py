from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import DraftModel
from packages.shared.types.quotation import QuotationDraft, ParsedQuotation, DraftStatus
import uuid
from datetime import datetime

class DraftService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_draft(self, draft_data: QuotationDraft) -> DraftModel:
        """Create a new quotation draft in the database."""
        db_draft = DraftModel(
            id=draft_data.id or str(uuid.uuid4()),
            customer_id=draft_data.customer_id,
            customer_match_score=draft_data.customer_match_score,
            customer_candidates=draft_data.customer_candidates,
            parsed_data=draft_data.parsed_data.model_dump(),
            material_matches=[m.model_dump() for m in draft_data.material_matches],
            status=DraftStatus(draft_data.status),
            needs_confirmation=draft_data.needs_confirmation,
            created_at=draft_data.created_at,
            updated_at=draft_data.updated_at
        )
        self.session.add(db_draft)
        await self.session.commit()
        await self.session.refresh(db_draft)
        return db_draft

    async def get_draft(self, draft_id: str) -> Optional[DraftModel]:
        """Get a draft by its ID."""
        result = await self.session.execute(select(DraftModel).where(DraftModel.id == draft_id))
        draft: Optional[DraftModel] = result.scalar_one_or_none()
        return draft

    async def list_drafts(self, limit: int = 100, offset: int = 0) -> List[DraftModel]:
        """List all drafts with pagination."""
        result = await self.session.execute(select(DraftModel).offset(offset).limit(limit).order_by(DraftModel.created_at.desc()))
        return list(result.scalars().all())

    async def update_draft(self, draft_id: str, update_data: Dict[str, Any]) -> Optional[DraftModel]:
        """Update a draft's information."""
        db_draft = await self.get_draft(draft_id)
        if not db_draft:
            return None

        for key, value in update_data.items():
            if hasattr(db_draft, key):
                setattr(db_draft, key, value)

        db_draft.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(db_draft)
        return db_draft
