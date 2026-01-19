from web3 import Web3
from app.core.config import settings

class Web3Client:
    w3 = None

def init_web3():
    Web3Client.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
    return Web3Client.w3

def get_web3():
    if not Web3Client.w3:
        init_web3()
    return Web3Client.w3
