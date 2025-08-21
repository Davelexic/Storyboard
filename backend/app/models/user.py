from __future__ import annotations
from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy import Column, JSON, DateTime, String, Boolean, Float, Integer
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


class UserPreferences(SQLModel, table=True):
    """Database model for user reading preferences."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    # Reading experience
    font_size: int = Field(default=16)
    brightness: float = Field(default=1.0)
    adaptive_brightness: bool = Field(default=False)
    
    # Effects configuration
    effects_enabled: bool = Field(default=True)
    effect_intensity: float = Field(default=0.5)
    effects_config: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # Accessibility
    high_contrast: bool = Field(default=False)
    reduce_motion: bool = Field(default=False)
    screen_reader_friendly: bool = Field(default=False)
    
    # Performance
    auto_save_progress: bool = Field(default=True)
    sync_preferences: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

