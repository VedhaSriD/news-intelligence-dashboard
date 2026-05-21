"""
core/config.py
Loads and validates all environment variables using Pydantic Settings.
Import get_settings() anywhere in the app — it is cached after first call.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_env:  str = "development"
    app_port: int = 8000
    cors_origins: str = "http://localhost:3000"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/news_intel"

    # External APIs
    newsapi_key:                str = ""
    google_factcheck_api_key:   str = ""
    openai_api_key:             str = ""

    # Clerk — used for verifying tokens from frontend
    clerk_secret_key: str = ""

    # Scheduler
    refresh_interval_hours: int = 6

    # Telegram (optional)
    telegram_bot_token: str = ""
    telegram_chat_id:   str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()