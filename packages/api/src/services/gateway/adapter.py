from typing import Protocol, runtime_checkable
from src.services.gateway.schemas import (
    QuotationDraft,
    QuotationUpdate,
    GatewayResponse,
    QuotationInfo,
)


@runtime_checkable
class GatewayAdapter(Protocol):
    async def create_draft(self, draft: QuotationDraft) -> GatewayResponse:
        """Create a new quotation draft in the legacy system."""
        ...

    async def update_quotation(
        self, external_id: str, update: QuotationUpdate
    ) -> GatewayResponse:
        """Update an existing quotation in the legacy system."""
        ...

    async def submit_quotation(self, external_id: str) -> GatewayResponse:
        """Submit a quotation for approval in the legacy system."""
        ...

    async def get_status(self, external_id: str) -> QuotationInfo:
        """Get the current status of a quotation from the legacy system."""
        ...
