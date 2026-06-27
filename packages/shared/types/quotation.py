from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class ParsedMaterial(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    raw_text: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class ParsedQuotation(BaseModel):
    customer_name: Optional[str] = None
    date: Optional[str] = None
    items: List[ParsedMaterial] = Field(default_factory=list)
    raw_text: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DraftStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SUBMITTED = "submitted"
    COMPLETED = "completed"

class MaterialMatch(BaseModel):
    material_id: Optional[str] = None
    score: float = 0.0
    candidates: List[Dict[str, Any]] = Field(default_factory=list)

class QuotationDraft(BaseModel):
    id: str = Field(description="Unique identifier for the draft")
    customer_id: Optional[str] = None
    customer_match_score: float = 0.0
    customer_candidates: List[Dict[str, Any]] = Field(default_factory=list)

    parsed_data: ParsedQuotation
    material_matches: List[MaterialMatch] = Field(default_factory=list)

    status: str = Field(default="draft", description="Status of the quotation")
    needs_confirmation: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
