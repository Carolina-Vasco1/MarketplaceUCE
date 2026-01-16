from fastapi import APIRouter, Depends

from app.schemas.blockchain import SmartContractResponse
from app.services.blockchain_service import BlockchainService
from app.deps.db import get_web3

router = APIRouter()

@router.get("/info")
async def get_contract_info(w3 = Depends(get_web3)):
    """Get smart contract information"""
    blockchain_service = BlockchainService(w3)
    info = await blockchain_service.get_contract_info()
    return info

@router.post("/call")
async def call_contract_function(
    function_name: str,
    params: dict,
    w3 = Depends(get_web3)
):
    """Call a contract function"""
    blockchain_service = BlockchainService(w3)
    result = await blockchain_service.call_contract_function(function_name, params)
    return result

@router.get("/events")
async def get_contract_events(
    limit: int = 10,
    w3 = Depends(get_web3)
):
    """Get contract events"""
    blockchain_service = BlockchainService(w3)
    events = await blockchain_service.get_contract_events(limit)
    return {"events": events}
