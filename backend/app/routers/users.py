from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register_user():
    """Placeholder endpoint for user registration."""
    return {"message": "User registration not yet implemented"}


@router.post("/login")
async def login_user():
    """Placeholder endpoint for user login."""
    return {"message": "User login not yet implemented"}
