from sqlalchemy import String, Integer, BigInteger, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class LedgerBlock(Base):
    __tablename__ = "ledger_blocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    index: Mapped[int] = mapped_column(Integer, nullable=False)

    prev_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    hash: Mapped[str] = mapped_column(String(128), nullable=False)

    topic: Mapped[str] = mapped_column(String(128), nullable=False)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)

    payload_json: Mapped[str] = mapped_column(Text, nullable=False)

    ts_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
