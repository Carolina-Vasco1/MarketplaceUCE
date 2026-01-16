from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
import time

from app.schemas.search import SearchQuery, SearchResponse
from app.services.search_service import SearchService
from app.deps.db import get_database

router = APIRouter()

@router.get("/products", response_model=SearchResponse)
async def search_products(
    q: str = Query(..., min_length=1),
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    rating: float = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Search products with filters"""
    start_time = time.time()
    
    search_query = SearchQuery(
        q=q,
        category=category,
        min_price=min_price,
        max_price=max_price,
        rating=rating,
        skip=skip,
        limit=limit
    )
    
    search_service = SearchService(db)
    results = await search_service.search(search_query)
    
    took_ms = int((time.time() - start_time) * 1000)
    
    return {
        "query": q,
        "total": len(results),
        "results": results,
        "took_ms": took_ms
    }

@router.get("/suggestions")
async def search_suggestions(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get search suggestions"""
    search_service = SearchService(db)
    suggestions = await search_service.get_suggestions(q, limit)
    return {"suggestions": suggestions}

@router.post("/index/rebuild")
async def rebuild_search_index(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Rebuild search index"""
    search_service = SearchService(db)
    await search_service.rebuild_index()
    return {"message": "Search index rebuilt successfully"}
