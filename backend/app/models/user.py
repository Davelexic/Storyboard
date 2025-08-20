from __future__ import annotations
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """Database model for application users."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    password: str

    books: List["Book"] = Relationship(back_populates="owner")
