import time
from typing import Optional
import structlog
from src.services.gateway.adapter import GatewayAdapter
from src.services.gateway.schemas import (
    QuotationDraft,
    QuotationUpdate,
    GatewayResponse,
    QuotationInfo,
)

logger = structlog.get_logger(__name__)


class GatewayClient:
    def __init__(self, adapter: GatewayAdapter) -> None:
        self.adapter = adapter

    async def create_draft(self, draft: QuotationDraft) -> GatewayResponse:
        start_time = time.perf_counter()
        log = logger.bind(method="create_draft", customer_name=draft.customer_name)
        try:
            response = await self.adapter.create_draft(draft)
            duration = time.perf_counter() - start_time
            log.info(
                "Gateway call completed",
                success=response.success,
                external_id=response.external_id,
                duration_ms=duration * 1000,
            )
            return response
        except Exception as e:
            duration = time.perf_counter() - start_time
            log.error(
                "Gateway call failed",
                error=str(e),
                duration_ms=duration * 1000,
            )
            raise

    async def update_quotation(
        self, external_id: str, update: QuotationUpdate
    ) -> GatewayResponse:
        start_time = time.perf_counter()
        log = logger.bind(method="update_quotation", external_id=external_id)
        try:
            response = await self.adapter.update_quotation(external_id, update)
            duration = time.perf_counter() - start_time
            log.info(
                "Gateway call completed",
                success=response.success,
                duration_ms=duration * 1000,
            )
            return response
        except Exception as e:
            duration = time.perf_counter() - start_time
            log.error(
                "Gateway call failed",
                error=str(e),
                duration_ms=duration * 1000,
            )
            raise

    async def submit_quotation(self, external_id: str) -> GatewayResponse:
        start_time = time.perf_counter()
        log = logger.bind(method="submit_quotation", external_id=external_id)
        try:
            response = await self.adapter.submit_quotation(external_id)
            duration = time.perf_counter() - start_time
            log.info(
                "Gateway call completed",
                success=response.success,
                duration_ms=duration * 1000,
            )
            return response
        except Exception as e:
            duration = time.perf_counter() - start_time
            log.error(
                "Gateway call failed",
                error=str(e),
                duration_ms=duration * 1000,
            )
            raise

    async def get_status(self, external_id: str) -> QuotationInfo:
        start_time = time.perf_counter()
        log = logger.bind(method="get_status", external_id=external_id)
        try:
            info = await self.adapter.get_status(external_id)
            duration = time.perf_counter() - start_time
            log.info(
                "Gateway call completed",
                status=info.status,
                duration_ms=duration * 1000,
            )
            return info
        except Exception as e:
            duration = time.perf_counter() - start_time
            log.error(
                "Gateway call failed",
                error=str(e),
                duration_ms=duration * 1000,
            )
            raise
