from fastapi import APIRouter, Depends

from app.schemas.blockchain import WalletResponse, WalletTransactionHistory
from app.services.blockchain_service import BlockchainService
from app.deps.db import get_web3

router = APIRouter()

@router.get("/{address}", response_model=WalletResponse)
async def get_wallet_info(
    address: str,
    w3 = Depends(get_web3)
):
    """Get wallet information"""
    blockchain_service = BlockchainService(w3)
    wallet_info = await blockchain_service.get_wallet_info(address)
    return wallet_info

@router.get("/{address}/balance")
async def get_wallet_balance(
    address: str,
    w3 = Depends(get_web3)
):
    """Get wallet balance"""
    blockchain_service = BlockchainService(w3)
    balance = await blockchain_service.get_wallet_balance(address)
    return {"address": address, "balance": balance}

@router.get("/{address}/history", response_model=WalletTransactionHistory)
async def get_wallet_history(
    address: str,
    limit: int = 50,
    w3 = Depends(get_web3)
):
    """Get wallet transaction history"""
    blockchain_service = BlockchainService(w3)
    history = await blockchain_service.get_wallet_history(address, limit)
    return history
