from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class LegacyQuotationStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class LegacyQuotationCreate(BaseModel):
    customer_id: str
    material_ids: List[str]
    external_id: Optional[str] = None

class LegacyQuotationUpdate(BaseModel):
    material_ids: Optional[List[str]] = None
    status: Optional[LegacyQuotationStatus] = None

class LegacyQuotationResponse(BaseModel):
    id: str
    customer_id: str
    material_ids: List[str]
    status: LegacyQuotationStatus
    created_at: datetime
    updated_at: datetime
