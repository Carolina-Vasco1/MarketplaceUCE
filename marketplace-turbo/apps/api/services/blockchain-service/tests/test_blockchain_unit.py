import pytest
from app.services.blockchain_service import BlockchainService

@pytest.mark.asyncio
async def test_send_transaction(blockchain_service):
    """Test sending transaction"""
    from app.schemas.blockchain import TransactionRequest
    tx = TransactionRequest(
        from_address="0x123",
        to_address="0x456",
        amount=1.5
    )
    result = await blockchain_service.send_transaction(tx)
    assert result.status == "pending"

@pytest.mark.asyncio
async def test_get_wallet_balance(blockchain_service):
    """Test getting wallet balance"""
    balance = await blockchain_service.get_wallet_balance("0x123")
    assert isinstance(balance, float)
    assert balance > 0
