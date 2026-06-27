import uuid
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Draft, DraftItem
from src.services.matching.engine import MatchingEngine
from src.services.notification.service import NotificationService
from shared.types.quotation import QuotationStatus

class DraftService:
    def __init__(self, db: AsyncSession, matching_engine: MatchingEngine, notification_service: NotificationService):
        self.db = db
        self.matching_engine = matching_engine
        self.notification_service = notification_service

    async def create_draft_from_ai_result(self, ai_data: Dict[str, Any]) -> Draft:
        customer_name = ai_data.get("customer_name", "Unknown")
        customer_matches = self.matching_engine.match_customer(customer_name)

        top_customer, customer_score = customer_matches[0] if customer_matches else (None, 0.0)

        draft_id = str(uuid.uuid4())
        draft = Draft(
            id=draft_id,
            customer_name_raw=customer_name,
            matched_customer_id=top_customer.id if top_customer and customer_score >= 0.85 else None,
            matching_score=customer_score,
            needs_confirmation=customer_score < 0.85,
            raw_data=ai_data,
            status=QuotationStatus.DRAFT
        )

        items_data = ai_data.get("items", [])
        total_needs_confirmation = draft.needs_confirmation

        for item_data in items_data:
            material_name = item_data.get("name", "")
            material_matches = self.matching_engine.match_material(material_name)
            top_material, material_score = material_matches[0] if material_matches else (None, 0.0)

            matched_id = top_material.id if top_material and material_score >= 0.85 else None
            if not matched_id:
                total_needs_confirmation = True

            item = DraftItem(
                material_name_raw=material_name,
                matched_material_id=matched_id,
                quantity=item_data.get("quantity", 1.0),
                unit_price=item_data.get("unit_price") or (top_material.unit_price if top_material else None),
                matching_score=material_score
            )
            draft.items.append(item)

        draft.needs_confirmation = total_needs_confirmation

        self.db.add(draft)
        await self.db.commit()
        await self.db.refresh(draft)

        await self.notification_service.send_draft_notification(
            draft.id,
            {"customer": customer_name, "score": customer_score, "needs_confirmation": draft.needs_confirmation}
        )

        return draft
