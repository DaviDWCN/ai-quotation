from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class QuotationItem(BaseModel):
    material_code: Optional[str] = Field(None, description="Material code or model name")
    quantity: Optional[float] = Field(None, description="Requested quantity")
    target_price: Optional[float] = Field(None, description="Target price")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    remarks: Optional[str] = Field(None, description="Item specific remarks")

class QuotationDraft(BaseModel):
    id: str = Field(description="Unique identifier for the draft")
    customer_id: Optional[str] = Field(None, description="ID of the customer (internal)")
    customer_name: Optional[str] = Field(None, description="Customer name from request")
    segmentation: Optional[str] = Field(None, description="Business segmentation/line")
    material_ids: List[str] = Field(default_factory=list, description="List of matched material IDs (internal)")
    items: List[QuotationItem] = Field(default_factory=list, description="Extracted material items")
    status: str = Field(default="DRAFT", description="Status of the quotation")
    delivery_date: Optional[str] = Field(None, description="Expected delivery date")
    remarks: Optional[str] = Field(None, description="General remarks")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
