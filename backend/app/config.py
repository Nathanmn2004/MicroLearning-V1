import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./microlearning.sqlite3")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    resend_api_key: str | None = os.getenv("RESEND_API_KEY")
    from_email: str = os.getenv("FROM_EMAIL", "Microaprendizagem <noreply@example.com>")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
    send_hour: int = int(os.getenv("SEND_HOUR", "7"))
    send_minute: int = int(os.getenv("SEND_MINUTE", "0"))
    content_epoch: str = os.getenv("CONTENT_EPOCH", "2026-01-01")
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
