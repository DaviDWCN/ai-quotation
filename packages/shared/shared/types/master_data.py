from pydantic import BaseModel, Field
from typing import Optional

class Customer(BaseModel):
    id: str = Field(description="Unique identifier for the customer")
    name: str = Field(description="Name of the customer")
    code: Optional[str] = Field(None, description="Customer code")
    email: Optional[str] = Field(None, description="Email of the customer")
    contact: Optional[str] = Field(None, description="Contact person")

class Material(BaseModel):
    id: str = Field(description="Unique identifier for the material")
    name: str = Field(description="Name of the material")
    code: Optional[str] = Field(None, description="Material code")
    category: Optional[str] = Field(None, description="Material category")
    spec: Optional[str] = Field(None, description="Specification")
    unit_price: float = Field(description="Unit price of the material")
