from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# SQLite URL for local development
DATABASE_URL = "sqlite:///./app.db"

# Needed for SQLite to allow usage from different threads
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
