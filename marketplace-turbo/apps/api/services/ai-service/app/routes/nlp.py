from fastapi import APIRouter, HTTPException, status

from app.schemas.ai import TextAnalysisRequest, TextAnalysisResponse
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/sentiment", response_model=TextAnalysisResponse)
async def analyze_sentiment(request: TextAnalysisRequest):
    """Analyze sentiment of text"""
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty"
        )
    
    ai_service = AIService()
    result = await ai_service.analyze_sentiment(request.text)
    return result

@router.post("/classify")
async def classify_text(request: TextAnalysisRequest):
    """Classify text into categories"""
    ai_service = AIService()
    result = await ai_service.classify_text(request.text)
    return result

@router.post("/extract-keywords")
async def extract_keywords(request: TextAnalysisRequest):
    """Extract keywords from text"""
    ai_service = AIService()
    keywords = await ai_service.extract_keywords(request.text)
    return {"text": request.text, "keywords": keywords}

@router.post("/generate-description")
async def generate_description(product_id: str):
    """Generate product description using AI"""
    ai_service = AIService()
    description = await ai_service.generate_product_description(product_id)
    return {"product_id": product_id, "description": description}
