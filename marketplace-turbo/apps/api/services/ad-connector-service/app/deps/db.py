from typing import Optional
from app.core.config import settings

class GoogleAdsClient:
    """Google Ads API Client wrapper"""
    
    def __init__(self):
        self.customer_id = settings.GOOGLE_ADS_CUSTOMER_ID
        self.api_key = settings.GOOGLE_ADS_API_KEY

class FacebookAdsClient:
    """Facebook Ads API Client wrapper"""
    
    def __init__(self):
        self.account_id = settings.FACEBOOK_ADS_ACCOUNT_ID
        self.access_token = settings.FACEBOOK_ADS_ACCESS_TOKEN
