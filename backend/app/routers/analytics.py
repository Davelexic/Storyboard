from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session
from ..models.analytics import AnalyticsEvent

router = APIRouter(prefix="/analytics", tags=["analytics"])


class EventIn(BaseModel):
    name: str
    payload: Dict[str, Any] = {}


class EventsBatch(BaseModel):
    events: List[EventIn]


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
