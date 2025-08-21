from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from sqlmodel import Session, select

from ..db import get_session
from ..models.analytics import AnalyticsEvent
from ..utils.sanitization import sanitize_string, sanitize_dict, SanitizationError

router = APIRouter(prefix="/analytics", tags=["analytics"])


class EventIn(BaseModel):
    name: str
    payload: Dict[str, Any] = {}
    
    @validator('name')
    def validate_name(cls, v):
        try:
            return sanitize_string(v, max_length=100)
        except SanitizationError as e:
            raise ValueError(str(e))
    
    @validator('payload')
    def validate_payload(cls, v):
        try:
            return sanitize_dict(v, max_length=50)  # Limit payload size
        except SanitizationError as e:
            raise ValueError(str(e))


class EventsBatch(BaseModel):
    events: List[EventIn]
    
    @validator('events')
    def validate_events(cls, v):
        if len(v) > 100:  # Limit batch size
            raise ValueError("Too many events in batch. Maximum: 100")
        return v


@router.post("/events")
def post_events(batch: EventsBatch, session: Session = Depends(get_session)):
    for evt in batch.events:
        session.add(AnalyticsEvent(name=evt.name, payload=evt.payload))
    session.commit()
    return {"status": "ok", "saved": len(batch.events)}


@router.get("/events")
def get_events(session: Session = Depends(get_session)):
    events = session.exec(select(AnalyticsEvent)).all()
    return events
