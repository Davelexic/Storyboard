from pydantic import BaseModel
import os


class Settings(BaseModel):
    """Application configuration loaded from environment variables."""

    database_url: str = os.getenv("DATABASE_URL")
    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    app_name: str = os.getenv("APP_NAME", "Cinematic Reading Engine")


settings = Settings()
