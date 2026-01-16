import pytest
from app.services.ad_service import AdService

@pytest.mark.asyncio
async def test_create_google_campaign(ad_service):
    """Test creating Google Ads campaign"""
    campaign = await ad_service.create_google_campaign(
        name="Test Campaign",
        budget=1000.0,
        keywords=["test", "campaign"],
        daily_budget=50.0
    )
    assert campaign["name"] == "Test Campaign"
    assert campaign["status"] == "active"

@pytest.mark.asyncio
async def test_list_campaigns(ad_service):
    """Test listing campaigns"""
    campaigns = await ad_service.list_campaigns(limit=10)
    assert len(campaigns) <= 10
