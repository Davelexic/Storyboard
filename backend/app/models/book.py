"""Data models for book-related operations.

Includes a placeholder model for uploaded books.
"""

from pydantic import BaseModel


class Book(BaseModel):
    """Represents an uploaded book."""

    id: int
    title: str
    author: str | None = None
