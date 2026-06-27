from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    missing: bool = False

class ExtractedNumberField(BaseModel):
    value: Optional[float] = None
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    missing: bool = False

class ExtractedItem(BaseModel):
    material_code: ExtractedField
    quantity: ExtractedNumberField
    unit: ExtractedField
    target_price: ExtractedNumberField

class AIParserOutput(BaseModel):
    customer_name: ExtractedField
    segmentation: ExtractedField
    items: List[ExtractedItem] = Field(default_factory=list)
    delivery_date: ExtractedField
    remarks: ExtractedField
