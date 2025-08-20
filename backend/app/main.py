from fastapi import FastAPI

from .db import init_db
from .routers import books, users

app = FastAPI(title="Cinematic Reading Engine")


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup."""
    init_db()

# Router includes
app.include_router(users.router)
app.include_router(books.router)


@app.get("/")
async def root():
    """Basic health check endpoint."""
    return {"status": "ok"}
