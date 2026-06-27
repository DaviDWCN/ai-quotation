from pydantic import BaseModel, Field

class Customer(BaseModel):
    id: str = Field(description="Unique identifier for the customer")
    name: str = Field(description="Name of the customer")
    email: str = Field(description="Email of the customer")

class Material(BaseModel):
    id: str = Field(description="Unique identifier for the material")
    name: str = Field(description="Name of the material")
    unit_price: float = Field(description="Unit price of the material")
