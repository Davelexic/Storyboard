from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = "sqlite:///./app.db"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    app_name: str = "Cinematic Reading Engine"

    class Config:
        env_file = ".env"


settings = Settings()
