from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class QuotationDraft(BaseModel):
    id: str = Field(description="Unique identifier for the draft")
    customer_id: str = Field(description="ID of the customer")
    material_ids: List[str] = Field(default_factory=list, description="List of material IDs involved")
    status: str = Field(default="DRAFT", description="Status of the quotation")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
