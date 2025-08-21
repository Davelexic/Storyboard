from pydantic import BaseModel
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables


class Settings(BaseModel):
    """Application configuration loaded from environment variables."""

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Security
    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.jwt_secret:
            raise ValueError(
                "JWT_SECRET environment variable must be set. "
                "Please set a secure secret key in your .env file or environment variables."
            )
    
    # API Configuration
    app_name: str = os.getenv("APP_NAME", "Cinematic Reading Engine")
    api_host: str = os.getenv("API_HOST", "localhost")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # Development
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # File Upload
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "52428800"))  # 50MB
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # Analysis Pipeline
    analysis_timeout: int = int(os.getenv("ANALYSIS_TIMEOUT", "300"))
    max_concurrent_analysis: int = int(os.getenv("MAX_CONCURRENT_ANALYSIS", "5"))
    
    # Effects Configuration
    default_effect_intensity: float = float(os.getenv("DEFAULT_EFFECT_INTENSITY", "0.5"))
    max_effects_per_chapter: int = int(os.getenv("MAX_EFFECTS_PER_CHAPTER", "3"))
    min_paragraphs_between_effects: int = int(os.getenv("MIN_PARAGRAPHS_BETWEEN_EFFECTS", "2"))


settings = Settings()
