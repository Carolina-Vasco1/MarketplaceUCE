from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from pymongo import TEXT
import re

from app.schemas.search import SearchQuery, ProductSearchResult

class SearchService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def search(self, query: SearchQuery) -> List[ProductSearchResult]:
        """Search products with filters"""
        collection = self.db["products"]
        
        filters = {
            "$text": {"$search": query.q}
        }
        
        if query.category:
            filters["category"] = query.category
        
        if query.min_price is not None:
            filters["price"] = {"$gte": query.min_price}
        
        if query.max_price is not None:
            if "price" in filters:
                filters["price"]["$lte"] = query.max_price
            else:
                filters["price"] = {"$lte": query.max_price}
        
        if query.rating is not None:
            filters["rating"] = {"$gte": query.rating}
        
        results = await collection.find(filters).skip(query.skip).limit(query.limit).to_list(query.limit)
        
        return [ProductSearchResult(**doc) for doc in results]
    
    async def get_suggestions(self, prefix: str, limit: int) -> List[str]:
        """Get search suggestions"""
        collection = self.db["products"]
        
        suggestions = await collection.distinct(
            "name",
            {"name": {"$regex": f"^{re.escape(prefix)}", "$options": "i"}}
        )
        
        return suggestions[:limit]
    
    async def rebuild_index(self) -> None:
        """Rebuild search indexes"""
        collection = self.db["products"]
        
        # Create text index
        await collection.create_index([("name", TEXT), ("description", TEXT)])
