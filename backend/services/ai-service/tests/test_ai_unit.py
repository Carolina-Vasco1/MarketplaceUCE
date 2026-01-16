import pytest
from app.services.ai_service import AIService

@pytest.mark.asyncio
async def test_get_recommendations(ai_service):
    """Test getting recommendations"""
    recommendations = await ai_service.get_user_recommendations("user1", limit=5)
    assert len(recommendations.recommendations) == 5

@pytest.mark.asyncio
async def test_analyze_sentiment(ai_service):
    """Test sentiment analysis"""
    result = await ai_service.analyze_sentiment("This product is amazing!")
    assert result.sentiment in ["positive", "negative", "neutral"]
    assert 0 <= result.confidence <= 1
