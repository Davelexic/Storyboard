from fastapi import FastAPI

from .config import settings
from .db import init_db
from .routers import books, users, analytics

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup."""
    init_db()

# Router includes
app.include_router(users.router)
app.include_router(books.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    """Basic health check endpoint."""
    return {"status": "ok"}
