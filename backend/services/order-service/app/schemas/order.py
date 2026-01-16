from pydantic import BaseModel, Field

class OrderIn(BaseModel):
    buyer_id: str
    product_id: str
    amount: float = Field(gt=0)

class OrderOut(OrderIn):
    id: str
    status: str
