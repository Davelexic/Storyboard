from fastapi import FastAPI

from .routers import books, users

app = FastAPI(title="Cinematic Reading Engine")

# Router includes
app.include_router(users.router)
app.include_router(books.router)


@app.get("/")
async def root():
    """Basic health check endpoint."""
    return {"status": "ok"}
