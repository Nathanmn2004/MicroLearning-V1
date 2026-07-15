from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "MicroAprendizagem"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api"

    frontend_url: str = "https://microaprendizagem.com.br"
    backend_url: str = "https://api.microaprendizagem.com.br"
    backend_cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "https://microaprendizagem.com.br"
    )

    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    database_url: str | None = None
    direct_url: str | None = None

    redis_url: str = "redis://localhost:6379/0"

    ai_provider: str = "gemini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    cakto_checkout_url: str | None = None
    cakto_webhook_secret: str | None = None

    resend_api_key: str | None = None
    resend_from_email: str | None = None
    resend_webhook_secret: str | None = None

    evolution_api_url: str | None = None
    evolution_api_key: str | None = None
    evolution_instance: str | None = None
    evolution_webhook_secret: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
