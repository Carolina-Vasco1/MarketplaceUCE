from fastapi import APIRouter, File, UploadFile, HTTPException, status

from app.schemas.ai import ImageAnalysisResponse
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/analyze-quality")
async def analyze_image_quality(image_url: str) -> ImageAnalysisResponse:
    """Analyze image quality"""
    ai_service = AIService()
    try:
        result = await ai_service.analyze_image_quality(image_url)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/detect-objects")
async def detect_objects(image_url: str):
    """Detect objects in image"""
    ai_service = AIService()
    objects = await ai_service.detect_objects(image_url)
    return {"image_url": image_url, "objects": objects}

@router.post("/extract-text")
async def extract_text_from_image(image_url: str):
    """Extract text from image"""
    ai_service = AIService()
    text = await ai_service.extract_text_from_image(image_url)
    return {"image_url": image_url, "extracted_text": text}

@router.post("/validate-product-image")
async def validate_product_image(image_url: str):
    """Validate if image is suitable for product listing"""
    ai_service = AIService()
    validation = await ai_service.validate_product_image(image_url)
    return {
        "image_url": image_url,
        "is_valid": validation["is_valid"],
        "issues": validation.get("issues", []),
        "recommendations": validation.get("recommendations", [])
    }
