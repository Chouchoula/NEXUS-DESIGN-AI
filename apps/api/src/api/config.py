"""
NEXUS DESIGN AI - Configuration Settings
"""

from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "NEXUS DESIGN AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    API_URL: str = "http://localhost:8000"
    APP_URL: str = "http://localhost:3000"

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    # Database
    DATABASE_URL: str = "postgresql+psycopg://nexus:nexus_dev@localhost:5432/nexus"
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI Providers
    DEFAULT_AI_PROVIDER: str = "anthropic"
    DEFAULT_AI_MODEL: str = ""
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    # Figma
    FIGMA_ACCESS_TOKEN: Optional[str] = None
    FIGMA_FILE_ID: Optional[str] = None

    # Visual Search
    BRAVE_SEARCH_API_KEY: Optional[str] = None
    UNSPLASH_ACCESS_KEY: Optional[str] = None
    PEXELS_API_KEY: Optional[str] = None

    # Security
    SECRET_KEY: str = "replace_with_a_long_random_secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./uploads"

    # Agent Settings
    AGENT_MAX_ITERATIONS: int = 10
    AGENT_TIMEOUT: int = 300
    MAX_CONCURRENT_AGENTS: int = 3

    # Token Budget
    MAX_TOKENS_PER_REQUEST: int = 100000
    TOTAL_TOKEN_BUDGET: Optional[int] = None

    # Visual QA
    PLAYWRIGHT_HEADLESS: bool = True
    VISUAL_QA_THRESHOLD: float = 0.95

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()