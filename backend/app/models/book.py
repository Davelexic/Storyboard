from __future__ import annotations
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel


class Book(SQLModel, table=True):
    """Database model for uploaded books."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: Optional[str] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    markup: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    owner: Optional["User"] = Relationship(back_populates="books")
