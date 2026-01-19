import json
import hashlib
import time
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, desc
from app.db.session import SessionLocal
from app.db.models import LedgerBlock

router = APIRouter(prefix="/api/v1/blockchain", tags=["blockchain"])

GENESIS_PREV = "0" * 64

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def compute_block_hash(index: int, prev_hash: str, topic: str, event_type: str, ts_ms: int, payload_json: str) -> str:
    base = f"{index}|{prev_hash}|{topic}|{event_type}|{ts_ms}|{payload_json}"
    return sha256_hex(base)

@router.get("/chain")
async def get_chain(limit: int = Query(50, ge=1, le=500)):
    async with SessionLocal() as session:
        rows = (await session.execute(select(LedgerBlock).order_by(desc(LedgerBlock.index)).limit(limit))).scalars().all()

    out = []
    for r in rows[::-1]:
        out.append({
            "index": r.index,
            "prev_hash": r.prev_hash,
            "hash": r.hash,
            "topic": r.topic,
            "event_type": r.event_type,
            "ts_ms": r.ts_ms,
            "payload": json.loads(r.payload_json),
        })
    return out

@router.get("/verify")
async def verify_chain():
    async with SessionLocal() as session:
        rows = (await session.execute(select(LedgerBlock).order_by(LedgerBlock.index.asc()))).scalars().all()

    if not rows:
        return {"ok": True, "blocks": 0, "message": "empty chain"}

    # Verificación encadenada + recomputar hashes
    prev_hash = GENESIS_PREV
    expected_index = 1

    for r in rows:
        if r.index != expected_index:
            return {"ok": False, "error": f"index mismatch at db_id={r.id}: expected {expected_index} got {r.index}"}

        if r.prev_hash != prev_hash:
            return {"ok": False, "error": f"prev_hash mismatch at index={r.index}"}

        recomputed = compute_block_hash(r.index, r.prev_hash, r.topic, r.event_type, r.ts_ms, r.payload_json)
        if recomputed != r.hash:
            return {"ok": False, "error": f"hash mismatch at index={r.index}"}

        prev_hash = r.hash
        expected_index += 1

    return {"ok": True, "blocks": len(rows)}

@router.post("/append")
async def append_manual(event: dict):
    """
    OPCIONAL: endpoint manual para pruebas (no lo uses en prod).
    El consumer Kafka es lo principal.
    """
    topic = event.get("topic", "manual")
    payload = event.get("payload", {})
    event_type = event.get("event_type", topic)

    payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    ts_ms = int(time.time() * 1000)

    async with SessionLocal() as session:
        last = (await session.execute(select(LedgerBlock).order_by(desc(LedgerBlock.index)).limit(1))).scalars().first()
        next_index = (last.index + 1) if last else 1
        prev_hash = last.hash if last else GENESIS_PREV

        h = compute_block_hash(next_index, prev_hash, topic, event_type, ts_ms, payload_json)

        b = LedgerBlock(
            index=next_index,
            prev_hash=prev_hash,
            hash=h,
            topic=topic,
            event_type=event_type,
            payload_json=payload_json,
            ts_ms=ts_ms,
        )
        session.add(b)
        await session.commit()

    return {"ok": True, "index": next_index, "hash": h}
