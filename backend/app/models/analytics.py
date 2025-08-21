from __future__ import annotations
from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


class AnalyticsEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    payload: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
