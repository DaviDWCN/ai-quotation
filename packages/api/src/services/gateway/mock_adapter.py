import asyncio
import random
import uuid
from datetime import datetime
from typing import Dict, Any, cast

from src.services.gateway.adapter import GatewayAdapter
from src.services.gateway.schemas import (
    QuotationDraft,
    QuotationUpdate,
    GatewayResponse,
    QuotationInfo,
    QuotationStatus,
)


class MockGatewayAdapter(GatewayAdapter):
    def __init__(self) -> None:
        self._db: Dict[str, Dict[str, Any]] = {}
        self._error_rate = 0.05
        self._min_latency = 0.2
        self._max_latency = 0.5

    async def _simulate_behavior(self) -> None:
        # Simulate latency
        latency = random.uniform(self._min_latency, self._max_latency)
        await asyncio.sleep(latency)

        # Simulate occasional error
        if random.random() < self._error_rate:
            raise Exception("Legacy System Error: 503 Service Unavailable")

    async def create_draft(self, draft: QuotationDraft) -> GatewayResponse:
        await self._simulate_behavior()

        external_id = f"LEG-{uuid.uuid4().hex[:8].upper()}"
        self._db[external_id] = {
            "external_id": external_id,
            "customer_name": draft.customer_name,
            "items": [item.model_dump() for item in draft.items],
            "total_amount": draft.total_amount,
            "remarks": draft.remarks,
            "status": QuotationStatus.DRAFT,
            "updated_at": datetime.now(),
        }

        return GatewayResponse(
            success=True,
            external_id=external_id,
            message="Draft created successfully",
            status=QuotationStatus.DRAFT,
        )

    async def update_quotation(
        self, external_id: str, update: QuotationUpdate
    ) -> GatewayResponse:
        await self._simulate_behavior()

        if external_id not in self._db:
            return GatewayResponse(
                success=False, message=f"Quotation {external_id} not found"
            )

        record = self._db[external_id]
        if update.items is not None:
            record["items"] = [item.model_dump() for item in update.items]
        if update.total_amount is not None:
            record["total_amount"] = update.total_amount
        if update.remarks is not None:
            record["remarks"] = update.remarks

        record["updated_at"] = datetime.now()

        return GatewayResponse(
            success=True,
            external_id=external_id,
            message="Quotation updated successfully",
            status=record["status"],
        )

    async def submit_quotation(self, external_id: str) -> GatewayResponse:
        await self._simulate_behavior()

        if external_id not in self._db:
            return GatewayResponse(
                success=False, message=f"Quotation {external_id} not found"
            )

        record = self._db[external_id]
        record["status"] = QuotationStatus.SUBMITTED
        record["updated_at"] = datetime.now()

        return GatewayResponse(
            success=True,
            external_id=external_id,
            message="Quotation submitted successfully",
            status=QuotationStatus.SUBMITTED,
        )

    async def get_status(self, external_id: str) -> QuotationInfo:
        await self._simulate_behavior()

        if external_id not in self._db:
            raise ValueError(f"Quotation {external_id} not found")

        record = self._db[external_id]

        # Simulate background status change (mocking legacy system approval)
        if record["status"] == QuotationStatus.SUBMITTED and random.random() < 0.3:
            record["status"] = QuotationStatus.APPROVED
            record["updated_at"] = datetime.now()

        return QuotationInfo(
            external_id=record["external_id"],
            status=record["status"],
            updated_at=record["updated_at"],
            raw_data=record,
        )
