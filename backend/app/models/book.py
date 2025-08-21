from __future__ import annotations
from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy import Column, JSON, DateTime
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    """Database model for uploaded books."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: Optional[str] = Field(default=None, index=True)
    language: Optional[str] = Field(default="en")
    identifier: Optional[str] = Field(default=None, index=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    
    # File metadata
    file_size: Optional[int] = Field(default=None)
    file_path: Optional[str] = Field(default=None)
    
    # Processing metadata
    markup: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    processing_status: str = Field(default="pending")  # pending, processing, completed, failed
    processing_error: Optional[str] = Field(default=None)
    
    # Analysis metadata
    theme: Optional[str] = Field(default=None)
    total_chapters: Optional[int] = Field(default=None)
    total_effects: Optional[int] = Field(default=None)
    effect_density: Optional[float] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    processed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    
    # Additional metadata
    book_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
