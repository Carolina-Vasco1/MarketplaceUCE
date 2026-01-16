from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import json
import uuid

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Event:
    event_id: str
    event_type: str
    occurred_at: str
    data: Dict[str, Any]
    trace_id: Optional[str] = None

    @staticmethod
    def create(event_type: str, data: Dict[str, Any], trace_id: Optional[str] = None) -> "Event":
        return Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            occurred_at=utc_now(),
            data=data,
            trace_id=trace_id,
        )

    def to_json(self) -> str:
        return json.dumps({
            "event_id": self.event_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at,
            "trace_id": self.trace_id,
            "data": self.data,
        }, ensure_ascii=False)
