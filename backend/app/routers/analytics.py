from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
from sqlmodel import Session, select

from ..db import get_session
from ..models.analytics import AnalyticsEvent
from ..models.user import User
from ..utils.sanitization import sanitize_string, sanitize_dict, SanitizationError
from ..middleware.auth import get_current_user

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
def post_events(
    batch: EventsBatch, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    for evt in batch.events:
        session.add(AnalyticsEvent(
            name=evt.name, 
            payload=evt.payload,
            user_id=current_user.id
        ))
    session.commit()
    return {"status": "ok", "saved": len(batch.events)}


@router.get("/events")
def get_events(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    events = session.exec(
        select(AnalyticsEvent)
        .where(AnalyticsEvent.user_id == current_user.id)
        .order_by(AnalyticsEvent.timestamp.desc())
    ).all()
    return events
