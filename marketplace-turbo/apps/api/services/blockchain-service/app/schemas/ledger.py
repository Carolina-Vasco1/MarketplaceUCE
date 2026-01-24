from pydantic import BaseModel

class BlockOut(BaseModel):
    index: int
    prev_hash: str
    hash: str
    topic: str
    event_type: str
    ts_ms: int
    payload: dict
