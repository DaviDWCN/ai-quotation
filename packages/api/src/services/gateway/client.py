import time
import structlog
from typing import List, Optional, Any, TypeVar, Callable, Awaitable, cast
from src.config import settings

from .adapter import GatewayAdapter
from .mock_adapter import MockGatewayAdapter
from .schemas import (
    LegacyQuotationCreate,
    LegacyQuotationUpdate,
    LegacyQuotationResponse,
    LegacyQuotationStatus
)

logger = structlog.get_logger(__name__)

T = TypeVar("T")

class IntegrationGateway:
    def __init__(self, adapter: Optional[GatewayAdapter] = None) -> None:
        if adapter:
            self.adapter = adapter
        elif settings.use_mock_gateway:
            self.adapter = MockGatewayAdapter()
        else:
            # Here we would initialize the real LegacySystemAdapter
            # For now, fallback to mock if not implemented
            self.adapter = MockGatewayAdapter()
            logger.warning("Real LegacySystemAdapter not implemented, falling back to mock")

    async def _call_with_logging(
        self, action: str, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any
    ) -> T:
        start_time = time.time()
        # Extract meaningful info for start log
        req_info = {"args": args, "kwargs": kwargs}
        logger.info(f"gateway_{action}_start", **req_info)

        try:
            response = await func(*args, **kwargs)
            duration = time.time() - start_time

            # Log success with full response
            resp_data: Any = None
            if hasattr(response, "model_dump"):
                resp_data = cast(Any, response).model_dump()
            elif isinstance(response, list):
                resp_data = [i.model_dump() if hasattr(i, "model_dump") else i for i in response]
            else:
                resp_data = response

            logger.info(
                f"gateway_{action}_success",
                duration=duration,
                response=resp_data
            )
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"gateway_{action}_failed",
                duration=duration,
                error=str(e),
                **req_info
            )
            raise

    async def create_draft(self, draft: LegacyQuotationCreate) -> LegacyQuotationResponse:
        return await self._call_with_logging(
            "create_draft", self.adapter.create_draft, draft
        )

    async def update_quotation(
        self, quotation_id: str, update: LegacyQuotationUpdate
    ) -> LegacyQuotationResponse:
        return await self._call_with_logging(
            "update_quotation", self.adapter.update_quotation, quotation_id, update
        )

    async def submit_quotation(self, quotation_id: str) -> LegacyQuotationResponse:
        return await self._call_with_logging(
            "submit_quotation", self.adapter.submit_quotation, quotation_id
        )

    async def get_quotation(self, quotation_id: str) -> LegacyQuotationResponse:
        return await self._call_with_logging(
            "get_quotation", self.adapter.get_quotation, quotation_id
        )

    async def list_quotations(
        self, status: Optional[LegacyQuotationStatus] = None
    ) -> List[LegacyQuotationResponse]:
        return await self._call_with_logging(
            "list_quotations", self.adapter.list_quotations, status=status
        )

# Singleton instance
gateway = IntegrationGateway()
