# backend/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General App Settings
    APP_NAME: str = "CarbonLens API"
    APP_ENV: str = "dev"

    # API Prefix
    API_PREFIX: str = "/api"

    # CORS Origins (allow all for now)
    CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env"  # Will load values from .env if exists
        extra = "ignore"    # Ignore extra values like CARBONLENS_API to avoid errors

settings = Settings()
