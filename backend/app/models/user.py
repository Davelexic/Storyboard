from __future__ import annotations
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Database model for application users."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str = Field(..., min_length=1)
    preferences: dict = Field(default_factory=dict, sa_column=Column(JSON))

