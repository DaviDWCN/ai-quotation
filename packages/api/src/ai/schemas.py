from typing import List, Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field
from src.ai.confidence import ConfidenceLevel

T = TypeVar("T")

class ExtractedField(BaseModel, Generic[T]):
    value: Optional[T] = None
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    missing: bool = False

class ExtractedItem(BaseModel):
    material_code: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))
    quantity: ExtractedField[float] = Field(default_factory=lambda: ExtractedField[float](missing=True))
    target_price: ExtractedField[float] = Field(default_factory=lambda: ExtractedField[float](missing=True))
    unit: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))
    remarks: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))

class ExtractedQuotation(BaseModel):
    customer_name: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))
    segmentation: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))
    items: List[ExtractedItem] = Field(default_factory=list)
    delivery_date: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))
    remarks: ExtractedField[str] = Field(default_factory=lambda: ExtractedField[str](missing=True))
