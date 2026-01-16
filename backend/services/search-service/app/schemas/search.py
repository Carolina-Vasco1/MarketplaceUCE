from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SearchQuery(BaseModel):
    q: str
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rating: Optional[float] = None
    skip: int = 0
    limit: int = 20

class ProductSearchResult(BaseModel):
    id: str
    name: str
    description: str
    price: float
    rating: float
    total_reviews: int
    category: str
    image_url: Optional[str] = None
    seller_id: str

class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[ProductSearchResult]
    took_ms: int
