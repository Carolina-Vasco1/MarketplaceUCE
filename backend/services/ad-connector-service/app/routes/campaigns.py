from fastapi import APIRouter, Depends, Query
from typing import List

from app.schemas.ads import CampaignResponse
from app.services.ad_service import AdService

router = APIRouter()

@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(
    platform: str = Query(None),
    status: str = Query(None),
    skip: int = 0,
    limit: int = 20
):
    """List ad campaigns"""
    ad_service = AdService()
    campaigns = await ad_service.list_campaigns(
        platform=platform,
        status=status,
        skip=skip,
        limit=limit
    )
    return campaigns

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str):
    """Get campaign details"""
    ad_service = AdService()
    campaign = await ad_service.get_campaign(campaign_id)
    return campaign

@router.get("/{campaign_id}/performance")
async def get_campaign_performance(
    campaign_id: str,
    date_from: str = Query(None),
    date_to: str = Query(None)
):
    """Get campaign performance data"""
    ad_service = AdService()
    performance = await ad_service.get_campaign_performance(
        campaign_id,
        date_from,
        date_to
    )
    return performance
