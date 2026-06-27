import time
from typing import Any, Dict, Optional
import structlog
from src.services.gateway.adapter import GatewayAdapter
from src.services.gateway.schemas import (
    GatewayQuotationCreate,
    GatewayQuotationUpdate,
    GatewayQuotationResponse,
    GatewayStatusResponse,
)

logger = structlog.get_logger(__name__)

class GatewayClient:
    def __init__(self, adapter: GatewayAdapter) -> None:
        self.adapter = adapter

    async def create_draft(self, data: GatewayQuotationCreate) -> GatewayQuotationResponse:
        result = await self._call_adapter("create_draft", data)
        return result  # type: ignore[no-any-return]

    async def update_quotation(
        self, quotation_id: str, data: GatewayQuotationUpdate
    ) -> GatewayQuotationResponse:
        result = await self._call_adapter("update_quotation", quotation_id, data)
        return result  # type: ignore[no-any-return]

    async def submit_quotation(self, quotation_id: str) -> GatewayQuotationResponse:
        result = await self._call_adapter("submit_quotation", quotation_id)
        return result  # type: ignore[no-any-return]

    async def get_status(self, quotation_id: str) -> GatewayStatusResponse:
        result = await self._call_adapter("get_status", quotation_id)
        return result  # type: ignore[no-any-return]

    async def _call_adapter(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        method = getattr(self.adapter, method_name)

        log = logger.bind(
            method=method_name,
            args=str(args),
            kwargs=str(kwargs)
        )

        try:
            result = await method(*args, **kwargs)
            duration = time.perf_counter() - start_time
            log.info(
                "gateway_call_success",
                duration_ms=round(duration * 1000, 2),
                response=str(result)
            )
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            log.error(
                "gateway_call_failed",
                duration_ms=round(duration * 1000, 2),
                error=str(e)
            )
            raise
