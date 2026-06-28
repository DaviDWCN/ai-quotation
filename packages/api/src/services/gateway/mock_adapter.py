import asyncio
import random
import uuid
from datetime import datetime, timezone
from typing import Dict

from src.services.gateway.adapter import GatewayAdapter
from src.services.gateway.schemas import (
    GatewayQuotationCreate,
    GatewayQuotationUpdate,
    GatewayQuotationResponse,
    GatewayStatusResponse,
    GatewayQuotationStatus,
)

class MockGatewayAdapter(GatewayAdapter):
    def __init__(self, enable_errors: bool = True, enable_delay: bool = True) -> None:
        self._storage: Dict[str, GatewayQuotationResponse] = {}
        self.enable_errors = enable_errors
        self.enable_delay = enable_delay

    async def _simulate_behavior(self) -> None:
        # Simulate delay (200-500ms)
        if self.enable_delay:
            delay = random.uniform(0.2, 0.5)
            await asyncio.sleep(delay)

        # Simulate occasional 503 errors (5%)
        if self.enable_errors and random.random() < 0.05:
            raise Exception("Mock Legacy System Error (503 Service Unavailable)")

    async def create_draft(self, data: GatewayQuotationCreate) -> GatewayQuotationResponse:
        await self._simulate_behavior()

        quotation_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        response = GatewayQuotationResponse(
            quotation_id=quotation_id,
            customer_id=data.customer_id,
            items=data.items,
            status=GatewayQuotationStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )
        self._storage[quotation_id] = response
        return response

    async def update_quotation(
        self, quotation_id: str, data: GatewayQuotationUpdate
    ) -> GatewayQuotationResponse:
        await self._simulate_behavior()

        if quotation_id not in self._storage:
            raise ValueError(f"Quotation {quotation_id} not found")

        quotation = self._storage[quotation_id]

        if data.items is not None:
            quotation.items = data.items
        if data.status is not None:
            quotation.status = data.status

        quotation.updated_at = datetime.now(timezone.utc)
        self._storage[quotation_id] = quotation
        return quotation

    async def submit_quotation(self, quotation_id: str) -> GatewayQuotationResponse:
        await self._simulate_behavior()

        if quotation_id not in self._storage:
            raise ValueError(f"Quotation {quotation_id} not found")

        quotation = self._storage[quotation_id]
        if quotation.status != GatewayQuotationStatus.DRAFT:
            raise ValueError(f"Cannot submit quotation in status {quotation.status}")

        quotation.status = GatewayQuotationStatus.SUBMITTED
        quotation.updated_at = datetime.now(timezone.utc)
        self._storage[quotation_id] = quotation
        return quotation

    async def get_status(self, quotation_id: str) -> GatewayStatusResponse:
        await self._simulate_behavior()

        if quotation_id not in self._storage:
            raise ValueError(f"Quotation {quotation_id} not found")

        quotation = self._storage[quotation_id]

        # Simulate background status change (legacy system side)
        if quotation.status == GatewayQuotationStatus.SUBMITTED:
            # 30% chance it gets approved/rejected when checked
            roll = random.random()
            if roll < 0.2:
                quotation.status = GatewayQuotationStatus.APPROVED
                quotation.updated_at = datetime.now(timezone.utc)
            elif roll < 0.3:
                quotation.status = GatewayQuotationStatus.REJECTED
                quotation.updated_at = datetime.now(timezone.utc)
            self._storage[quotation_id] = quotation

        return GatewayStatusResponse(
            quotation_id=quotation.quotation_id,
            status=quotation.status,
            updated_at=quotation.updated_at,
        )
