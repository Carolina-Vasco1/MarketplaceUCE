from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CampaignCreate(BaseModel):
    name: str
    platform: str  # google_ads, facebook_ads
    budget: float
    start_date: datetime
    end_date: datetime
    target_audience: dict
    keywords: Optional[List[str]] = None
    ad_copy: str

class CampaignResponse(BaseModel):
    id: str
    name: str
    platform: str
    budget: float
    spent: float
    impressions: int
    clicks: int
    conversions: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CampaignMetrics(BaseModel):
    campaign_id: str
    impressions: int
    clicks: int
    conversions: int
    ctr: float  # Click Through Rate
    cpc: float  # Cost Per Click
    roas: float  # Return On Ad Spend

class GoogleAdsResponse(BaseModel):
    campaign_id: str
    google_campaign_id: str
    status: str
    budget: float
    metrics: CampaignMetrics

class FacebookAdsResponse(BaseModel):
    campaign_id: str
    facebook_campaign_id: str
    status: str
    budget: float
    metrics: CampaignMetrics
