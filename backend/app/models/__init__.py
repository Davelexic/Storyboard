"""Database models used by the application."""

from .user import User  # noqa: F401
from .book import Book  # noqa: F401

__all__ = ["User", "Book"]
