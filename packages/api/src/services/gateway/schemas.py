from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class GatewayQuotationStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class GatewayQuotationItem(BaseModel):
    material_id: str
    quantity: float
    price: Optional[float] = None

class GatewayQuotationCreate(BaseModel):
    customer_id: str
    items: List[GatewayQuotationItem]

class GatewayQuotationUpdate(BaseModel):
    items: Optional[List[GatewayQuotationItem]] = None
    status: Optional[GatewayQuotationStatus] = None

class GatewayQuotationResponse(BaseModel):
    quotation_id: str
    customer_id: str
    items: List[GatewayQuotationItem]
    status: GatewayQuotationStatus
    created_at: datetime
    updated_at: datetime

class GatewayStatusResponse(BaseModel):
    quotation_id: str
    status: GatewayQuotationStatus
    updated_at: datetime
