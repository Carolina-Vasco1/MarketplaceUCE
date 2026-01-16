from fastapi import APIRouter, Depends
from typing import List

from app.schemas.ai import ProductRecommendationRequest, RecommendationResponse
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/for-user", response_model=RecommendationResponse)
async def get_recommendations_for_user(request: ProductRecommendationRequest):
    """Get product recommendations for a user"""
    ai_service = AIService()
    recommendations = await ai_service.get_user_recommendations(
        request.user_id,
        request.limit,
        request.category
    )
    return recommendations

@router.post("/similar-products")
async def get_similar_products(product_id: str, limit: int = 5):
    """Get similar products"""
    ai_service = AIService()
    similar = await ai_service.get_similar_products(product_id, limit)
    return {"product_id": product_id, "similar_products": similar}

@router.post("/trending")
async def get_trending_products(limit: int = 10, category: str = None):
    """Get trending products"""
    ai_service = AIService()
    trending = await ai_service.get_trending_products(limit, category)
    return {"trending": trending, "category": category}
