from __future__ import annotations
from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy import Column, JSON, DateTime
from sqlmodel import Field, SQLModel


def default_preferences() -> dict:
    """Default nested preferences for a new user."""
    return {
        "effectsEnabled": True,
        "fontSize": 16,
        "brightness": 1.0,
        "adaptiveBrightness": False,
        "effects": {
            "motion": {"enabled": True, "intensity": 1.0},
            "color": {"enabled": True, "intensity": 1.0},
        },
    }


class User(SQLModel, table=True):
    """Database model for users."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    preferences: Dict[str, Any] = Field(
        default_factory=default_preferences, sa_column=Column(JSON)
    )




