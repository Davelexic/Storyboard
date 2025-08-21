from __future__ import annotations
from typing import Optional

from sqlalchemy import Column, JSON
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
    """Database model for application users."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str = Field(..., min_length=1)
    preferences: dict = Field(
        default_factory=default_preferences, sa_column=Column(JSON)
    )

