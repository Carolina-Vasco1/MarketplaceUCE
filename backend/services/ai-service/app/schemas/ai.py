from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductRecommendationRequest(BaseModel):
    user_id: str
    limit: int = 10
    category: Optional[str] = None

class Product(BaseModel):
    id: str
    name: str
    price: float
    rating: float
    score: float  # Recommendation score

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[Product]
    generated_at: datetime

class TextAnalysisRequest(BaseModel):
    text: str
    analysis_type: str  # sentiment, category, keywords

class TextAnalysisResponse(BaseModel):
    text: str
    sentiment: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[List[str]] = None
    confidence: float

class ImageAnalysisRequest(BaseModel):
    image_url: str
    analysis_type: str  # quality, objects, text_extraction

class ImageAnalysisResponse(BaseModel):
    image_url: str
    quality_score: float
    detected_objects: List[str]
    has_text: bool
    extracted_text: Optional[str] = None
