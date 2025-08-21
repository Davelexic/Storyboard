from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .routers import books, users, analytics

app = FastAPI(title=settings.app_name)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",  # React development server alternative
        "http://localhost:8081",  # React Native development server
        "http://127.0.0.1:8081",  # React Native development server alternative
        "exp://localhost:19000",  # Expo development server
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


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
