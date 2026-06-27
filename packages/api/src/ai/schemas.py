from pydantic import BaseModel, Field
from typing import List, Optional
from packages.shared.types.quotation import ConfidenceLevel

class ExtractedItem(BaseModel):
    material_code: Optional[str] = Field(None, description="物料编码/型号")
    quantity: Optional[float] = Field(None, description="需求数量")
    unit: Optional[str] = Field(None, description="单位")
    target_price: Optional[float] = Field(None, description="目标价")
    confidence: ConfidenceLevel = Field(ConfidenceLevel.LOW)
    missing: bool = Field(False)

class ExtractedQuotation(BaseModel):
    customer_name: Optional[str] = Field(None, description="客户名称")
    segmentation: Optional[str] = Field(None, description="产品线/业务分类")
    items: List[ExtractedItem] = Field(default_factory=list)
    delivery_date: Optional[str] = Field(None, description="期望交期")
    remarks: Optional[str] = Field(None, description="备注")
    confidence_scores: dict[str, ConfidenceLevel] = Field(default_factory=dict)
