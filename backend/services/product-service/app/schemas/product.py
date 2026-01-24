from pydantic import BaseModel, Field
from typing import List

class ProductIn(BaseModel):
    title: str
    description: str
    price: float = Field(gt=0)
    category_id: str
    seller_id: str
    images: List[str] = []

class ProductOut(ProductIn):
    id: str
    status: str = "active"
