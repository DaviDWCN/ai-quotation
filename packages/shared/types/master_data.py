from pydantic import BaseModel, Field
from typing import Optional

class Customer(BaseModel):
    id: str = Field(description="Unique identifier for the customer")
    name: str = Field(description="Name of the customer")
    code: Optional[str] = Field(None, description="Internal customer code")
    contact: Optional[str] = Field(None, description="Contact person or information")
    email: Optional[str] = Field(None, description="Email of the customer")

class Material(BaseModel):
    id: str = Field(description="Unique identifier for the material")
    name: str = Field(description="Name of the material")
    code: Optional[str] = Field(None, description="Internal material code")
    specification: Optional[str] = Field(None, description="Technical specification")
    unit: Optional[str] = Field(None, description="Measurement unit (e.g., PCS, KG)")
    unit_price: float = Field(description="Unit price of the material")
