from typing import Protocol, runtime_checkable
from src.services.gateway.schemas import (
    GatewayQuotationCreate,
    GatewayQuotationUpdate,
    GatewayQuotationResponse,
    GatewayStatusResponse,
)

@runtime_checkable
class GatewayAdapter(Protocol):
    async def create_draft(self, data: GatewayQuotationCreate) -> GatewayQuotationResponse:
        """Create a new quotation draft in the legacy system."""
        ...

    async def update_quotation(
        self, quotation_id: str, data: GatewayQuotationUpdate
    ) -> GatewayQuotationResponse:
        """Update an existing quotation in the legacy system."""
        ...

    async def submit_quotation(self, quotation_id: str) -> GatewayQuotationResponse:
        """Submit a quotation for approval in the legacy system."""
        ...

    async def get_status(self, quotation_id: str) -> GatewayStatusResponse:
        """Get the current status of a quotation from the legacy system."""
        ...
