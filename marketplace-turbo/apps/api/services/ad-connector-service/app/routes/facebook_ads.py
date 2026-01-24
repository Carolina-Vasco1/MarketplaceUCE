from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.ads import FacebookAdsResponse, CampaignMetrics
from app.services.ad_service import AdService

router = APIRouter()

@router.post("/campaigns", response_model=FacebookAdsResponse)
async def create_facebook_campaign(
    name: str,
    budget: float,
    audience: dict,
    daily_budget: float
):
    """Create a Facebook Ads campaign"""
    try:
        ad_service = AdService()
        campaign = await ad_service.create_facebook_campaign(
            name=name,
            budget=budget,
            audience=audience,
            daily_budget=daily_budget
        )
        return campaign
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/campaigns/{campaign_id}/metrics", response_model=CampaignMetrics)
async def get_facebook_campaign_metrics(campaign_id: str):
    """Get Facebook Ads campaign metrics"""
    ad_service = AdService()
    metrics = await ad_service.get_facebook_metrics(campaign_id)
    return metrics

@router.put("/campaigns/{campaign_id}")
async def update_facebook_campaign(
    campaign_id: str,
    budget: float,
    status: str
):
    """Update Facebook Ads campaign"""
    ad_service = AdService()
    updated = await ad_service.update_facebook_campaign(campaign_id, budget, status)
    return updated

@router.delete("/campaigns/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_facebook_campaign(campaign_id: str):
    """Delete Facebook Ads campaign"""
    ad_service = AdService()
    await ad_service.delete_facebook_campaign(campaign_id)
    return None
