from typing import List, Optional, Dict
from datetime import datetime
import random

from app.schemas.ai import RecommendationResponse, Product, TextAnalysisResponse, ImageAnalysisResponse

class AIService:
    """AI Service for recommendations, NLP, and image analysis"""
    
    async def get_user_recommendations(self, user_id: str, limit: int = 10, category: Optional[str] = None) -> RecommendationResponse:
        """Generate product recommendations for a user"""
        # Mock recommendation logic
        recommendations = [
            Product(
                id=f"prod_{i}",
                name=f"Recommended Product {i}",
                price=99.99 + (i * 10),
                rating=4.5 + (i * 0.1),
                score=0.95 - (i * 0.05)
            )
            for i in range(limit)
        ]
        
        return RecommendationResponse(
            user_id=user_id,
            recommendations=recommendations,
            generated_at=datetime.now()
        )
    
    async def get_similar_products(self, product_id: str, limit: int = 5) -> List[Product]:
        """Get similar products based on features"""
        similar = [
            Product(
                id=f"similar_{i}",
                name=f"Similar Product {i}",
                price=99.99,
                rating=4.3,
                score=0.92 - (i * 0.05)
            )
            for i in range(limit)
        ]
        return similar
    
    async def get_trending_products(self, limit: int = 10, category: Optional[str] = None) -> List[Product]:
        """Get trending products"""
        trending = [
            Product(
                id=f"trend_{i}",
                name=f"Trending Product {i}",
                price=79.99 + (i * 5),
                rating=4.7,
                score=0.98 - (i * 0.02)
            )
            for i in range(limit)
        ]
        return trending
    
    async def analyze_sentiment(self, text: str) -> TextAnalysisResponse:
        """Analyze sentiment of text"""
        # Mock sentiment analysis
        sentiments = ["positive", "negative", "neutral"]
        sentiment = sentiments[len(text) % 3]
        confidence = 0.85 + random.uniform(0, 0.15)
        
        return TextAnalysisResponse(
            text=text,
            sentiment=sentiment,
            confidence=confidence
        )
    
    async def classify_text(self, text: str) -> Dict:
        """Classify text into categories"""
        categories = ["Electronics", "Fashion", "Home", "Sports", "Books"]
        category = categories[len(text) % len(categories)]
        confidence = 0.82 + random.uniform(0, 0.18)
        
        return {
            "text": text[:100],
            "category": category,
            "confidence": confidence
        }
    
    async def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        words = text.split()
        keywords = [w for w in words if len(w) > 3][:5]
        return keywords if keywords else ["keyword1", "keyword2"]
    
    async def generate_product_description(self, product_id: str) -> str:
        """Generate product description using AI"""
        return f"Premium quality product designed for excellence. Perfect for everyday use with exceptional durability and style."
    
    async def analyze_image_quality(self, image_url: str) -> ImageAnalysisResponse:
        """Analyze image quality"""
        quality_score = 0.85 + random.uniform(-0.1, 0.15)
        
        return ImageAnalysisResponse(
            image_url=image_url,
            quality_score=min(1.0, quality_score),
            detected_objects=["product", "background"],
            has_text=False,
            extracted_text=None
        )
    
    async def detect_objects(self, image_url: str) -> List[str]:
        """Detect objects in image"""
        return ["person", "product", "shelf", "background"]
    
    async def extract_text_from_image(self, image_url: str) -> Optional[str]:
        """Extract text from image"""
        return "Sample text extracted from image"
    
    async def validate_product_image(self, image_url: str) -> Dict:
        """Validate if image is suitable for product listing"""
        quality_score = 0.88 + random.uniform(-0.1, 0.12)
        
        is_valid = quality_score > 0.7
        issues = [] if is_valid else ["Low brightness", "Poor contrast"]
        recommendations = ["Adjust lighting", "Use better camera"] if quality_score < 0.9 else []
        
        return {
            "is_valid": is_valid,
            "quality_score": quality_score,
            "issues": issues,
            "recommendations": recommendations
        }
