from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from enum import Enum

class QuotationStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SUBMITTED = "submitted"
    COMPLETED = "completed"

class QuotationItem(BaseModel):
    material_name_raw: str = Field(description="Raw material name from AI")
    matched_material_id: Optional[str] = Field(None, description="Matched material ID from master data")
    quantity: float = Field(default=1.0)
    unit_price: Optional[float] = Field(None)
    matching_score: float = Field(default=0.0)

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class QuotationDraft(BaseModel):
    id: str = Field(description="Unique identifier for the draft")
    customer_name_raw: str = Field(description="Raw customer name from AI")
    matched_customer_id: Optional[str] = Field(None, description="Matched customer ID from master data")
    items: List[QuotationItem] = Field(default_factory=list)
    status: QuotationStatus = Field(default=QuotationStatus.DRAFT)
    matching_score: float = Field(default=0.0)
    needs_confirmation: bool = Field(default=True)
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Full AI output")
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
