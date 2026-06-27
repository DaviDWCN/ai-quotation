import asyncio
import random
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict
from fastapi import HTTPException

from .adapter import GatewayAdapter
from .schemas import (
    LegacyQuotationCreate,
    LegacyQuotationUpdate,
    LegacyQuotationResponse,
    LegacyQuotationStatus
)

class MockGatewayAdapter(GatewayAdapter):
    def __init__(self) -> None:
        self._storage: Dict[str, LegacyQuotationResponse] = {}

    async def _simulate_behavior(self) -> None:
        # Simulate delay 200-500ms
        await asyncio.sleep(random.uniform(0.2, 0.5))

        # Simulate 5% failure rate
        if random.random() < 0.05:
            raise HTTPException(status_code=503, detail="Service Unavailable (Mock Failure)")

    async def create_draft(self, draft: LegacyQuotationCreate) -> LegacyQuotationResponse:
        await self._simulate_behavior()

        quotation_id = f"LEG-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        response = LegacyQuotationResponse(
            id=quotation_id,
            customer_id=draft.customer_id,
            material_ids=draft.material_ids,
            status=LegacyQuotationStatus.DRAFT,
            created_at=now,
            updated_at=now
        )
        self._storage[quotation_id] = response
        return response

    async def update_quotation(
        self, quotation_id: str, update: LegacyQuotationUpdate
    ) -> LegacyQuotationResponse:
        await self._simulate_behavior()

        if quotation_id not in self._storage:
            raise HTTPException(status_code=404, detail="Quotation not found")

        quotation = self._storage[quotation_id]

        if update.material_ids is not None:
            quotation.material_ids = update.material_ids
        if update.status is not None:
            quotation.status = update.status

        quotation.updated_at = datetime.now(timezone.utc)
        self._storage[quotation_id] = quotation
        return quotation

    async def submit_quotation(self, quotation_id: str) -> LegacyQuotationResponse:
        await self._simulate_behavior()

        if quotation_id not in self._storage:
            raise HTTPException(status_code=404, detail="Quotation not found")

        quotation = self._storage[quotation_id]
        quotation.status = LegacyQuotationStatus.SUBMITTED
        quotation.updated_at = datetime.now(timezone.utc)

        # Simulate legacy system auto-approval after some time (not implemented here, but could be)

        self._storage[quotation_id] = quotation
        return quotation

    async def get_quotation(self, quotation_id: str) -> LegacyQuotationResponse:
        await self._simulate_behavior()

        if quotation_id not in self._storage:
            raise HTTPException(status_code=404, detail="Quotation not found")

        return self._storage[quotation_id]

    async def list_quotations(
        self, status: Optional[LegacyQuotationStatus] = None
    ) -> List[LegacyQuotationResponse]:
        await self._simulate_behavior()

        results = list(self._storage.values())
        if status:
            results = [r for r in results if r.status == status]

        return results
