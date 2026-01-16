from pydantic import BaseModel

class CategoryIn(BaseModel):
    name: str

class CategoryOut(CategoryIn):
    id: str
