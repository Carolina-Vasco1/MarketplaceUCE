import pytest

@pytest.mark.asyncio
async def test_search_products(search_service):
    """Test searching products"""
    query = "laptop"
    results = await search_service.search(query)
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_search_suggestions(search_service):
    """Test search suggestions"""
    suggestions = await search_service.get_suggestions("lapt", limit=5)
    assert isinstance(suggestions, list)
