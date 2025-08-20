from __future__ import annotations
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """Database model for application users."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True)
    hashed_password: str = Field(..., min_length=1)

    books: List["Book"] = Relationship(back_populates="owner")
