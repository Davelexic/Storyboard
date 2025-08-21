"""Database models used by the application."""

from sqlmodel import SQLModel
from .user import User  # noqa: F401
from .book import Book  # noqa: F401
from .analytics import AnalyticsEvent  # noqa: F401

__all__ = ["SQLModel", "User", "Book", "AnalyticsEvent"]
