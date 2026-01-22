from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime

from app.db.session import Base

class LedgerBlock(Base):
    __tablename__ = "ledger_blocks"

    order_id = Column(String, primary_key=True)
    hash = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
