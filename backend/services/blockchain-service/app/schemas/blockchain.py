from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionRequest(BaseModel):
    from_address: str
    to_address: str
    amount: float
    gas_limit: int = 21000

class TransactionResponse(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    status: str  # pending, confirmed, failed
    created_at: datetime

class SmartContractResponse(BaseModel):
    contract_address: str
    network: str
    deployed_at: datetime
    status: str  # active, paused

class WalletResponse(BaseModel):
    address: str
    balance: float
    total_transactions: int
    created_at: datetime

class WalletTransactionHistory(BaseModel):
    address: str
    transactions: list
    total_volume: float
