from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.blockchain import TransactionRequest, TransactionResponse
from app.services.blockchain_service import BlockchainService
from app.deps.db import get_web3

router = APIRouter()

@router.post("/send", response_model=TransactionResponse)
async def send_transaction(
    transaction: TransactionRequest,
    w3 = Depends(get_web3)
):
    """Send a transaction on blockchain"""
    try:
        blockchain_service = BlockchainService(w3)
        result = await blockchain_service.send_transaction(transaction)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{tx_hash}")
async def get_transaction_status(
    tx_hash: str,
    w3 = Depends(get_web3)
):
    """Get transaction status"""
    blockchain_service = BlockchainService(w3)
    status = await blockchain_service.get_transaction_status(tx_hash)
    return status

@router.get("/list/{address}")
async def list_transactions(
    address: str,
    limit: int = 10,
    w3 = Depends(get_web3)
):
    """List transactions for an address"""
    blockchain_service = BlockchainService(w3)
    transactions = await blockchain_service.list_transactions(address, limit)
    return {"address": address, "transactions": transactions}
