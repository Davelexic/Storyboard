from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from .config import settings

# Database engine configured via settings.database_url

# Needed for SQLite to allow usage from different threads
connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, echo=True, connect_args=connect_args)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def init_db() -> None:
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)
