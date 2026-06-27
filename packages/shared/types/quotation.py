from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class QuotationItem(BaseModel):
    material_code: Optional[str] = Field(None, description="Material code or model")
    quantity: Optional[float] = Field(None, description="Required quantity")
    unit: Optional[str] = Field(None, description="Unit")
    target_price: Optional[float] = Field(None, description="Target price")

    # Metadata for AI extraction
    confidence: Optional[str] = Field(None, description="Confidence level (high/medium/low)")
    missing: bool = Field(default=False)

class QuotationDraft(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the draft")
    customer_name: Optional[str] = Field(None, description="Customer name")
    segmentation: Optional[str] = Field(None, description="Product line or business segmentation")
    items: List[QuotationItem] = Field(default_factory=list, description="List of quotation items")
    delivery_date: Optional[str] = Field(None, description="Expected delivery date")
    remarks: Optional[str] = Field(None, description="Remarks")

    # Metadata for AI extraction
    confidence: Optional[str] = Field(None, description="Overall confidence level")
    status: str = Field(default="DRAFT", description="Status of the quotation")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
