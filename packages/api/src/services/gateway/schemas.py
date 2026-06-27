from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class QuotationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class QuotationItem(BaseModel):
    item_code: str
    description: str
    quantity: float
    unit_price: Optional[float] = None
    currency: str = "CNY"


class QuotationDraft(BaseModel):
    external_id: Optional[str] = None
    customer_name: str
    items: List[QuotationItem]
    total_amount: Optional[float] = None
    remarks: Optional[str] = None


class QuotationUpdate(BaseModel):
    items: Optional[List[QuotationItem]] = None
    total_amount: Optional[float] = None
    remarks: Optional[str] = None


class GatewayResponse(BaseModel):
    success: bool
    external_id: Optional[str] = None
    message: Optional[str] = None
    status: Optional[QuotationStatus] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class QuotationInfo(BaseModel):
    external_id: str
    status: QuotationStatus
    updated_at: datetime
    raw_data: Optional[dict[str, object]] = None
