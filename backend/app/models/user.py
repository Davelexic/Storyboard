"""Data models for user-related operations.

Currently includes a simple Pydantic model as a placeholder.
"""

from pydantic import BaseModel


class User(BaseModel):
    """Represents a registered user."""

    id: int
    email: str
    password: str
