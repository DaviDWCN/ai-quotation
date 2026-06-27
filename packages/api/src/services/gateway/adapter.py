from typing import Protocol, List, Optional
from .schemas import (
    LegacyQuotationCreate,
    LegacyQuotationUpdate,
    LegacyQuotationResponse,
    LegacyQuotationStatus
)

class GatewayAdapter(Protocol):
    async def create_draft(self, draft: LegacyQuotationCreate) -> LegacyQuotationResponse:
        ...

    async def update_quotation(
        self, quotation_id: str, update: LegacyQuotationUpdate
    ) -> LegacyQuotationResponse:
        ...

    async def submit_quotation(self, quotation_id: str) -> LegacyQuotationResponse:
        ...

    async def get_quotation(self, quotation_id: str) -> LegacyQuotationResponse:
        ...

    async def list_quotations(
        self, status: Optional[LegacyQuotationStatus] = None
    ) -> List[LegacyQuotationResponse]:
        ...
