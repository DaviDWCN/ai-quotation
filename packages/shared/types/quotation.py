from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class QuotationItem(BaseModel):
    material_code: Optional[str] = Field(None, description="物料编码/型号")
    quantity: Optional[float] = Field(None, description="需求数量")
    unit: Optional[str] = Field(None, description="单位")
    target_price: Optional[float] = Field(None, description="目标价")
    confidence: Optional[ConfidenceLevel] = Field(None, description="置信度")
    missing: bool = Field(False, description="是否缺失必填字段")

class QuotationDraft(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the draft")
    customer_id: Optional[str] = Field(None, description="ID of the customer")
    customer_name: Optional[str] = Field(None, description="客户名称")
    segmentation: Optional[str] = Field(None, description="产品线/业务分类")
    items: List[QuotationItem] = Field(default_factory=list, description="物料明细列表")
    delivery_date: Optional[str] = Field(None, description="期望交期")
    remarks: Optional[str] = Field(None, description="备注")
    status: str = Field(default="DRAFT", description="Status of the quotation")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confidence_scores: dict[str, ConfidenceLevel] = Field(default_factory=dict, description="字段级置信度评分")
    material_ids: List[str] = Field(default_factory=list, description="List of material IDs involved")
