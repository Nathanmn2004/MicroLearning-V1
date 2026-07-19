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
    gemini_model: str = "gemini-3.5-flash"

    cakto_checkout_url: str | None = None
    cakto_checkout_url_mente_desenvolvimento_pessoal: str | None = None
    cakto_checkout_url_carreira_negocios_dinheiro: str | None = None
    cakto_checkout_url_historia_sociedade: str | None = None
    cakto_webhook_secret: str | None = None

    resend_api_key: str | None = None
    resend_from_email: str | None = None
    resend_webhook_secret: str | None = None

    evolution_api_url: str | None = None
    evolution_api_key: str | None = None
    evolution_instance: str | None = None
    evolution_webhook_secret: str | None = None

    content_delivery_frequency: str = "daily"
    content_delivery_time: str = "09:00"
    content_delivery_timezone: str = "America/Sao_Paulo"
    content_delivery_channels: str = "email"
    content_delivery_lesson_statuses: str = "review,approved"
    content_delivery_batch_limit: int = 50
    generated_lesson_status: str = "approved"

    valid_content_tracks: str = (
        "todos,"
        "mente-desenvolvimento-pessoal,"
        "carreira-negocios-dinheiro,"
        "historia-sociedade"
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def delivery_channels(self) -> list[str]:
        return [
            channel.strip().lower()
            for channel in self.content_delivery_channels.split(",")
            if channel.strip()
        ]

    @property
    def delivery_lesson_statuses(self) -> list[str]:
        return [
            status.strip().lower()
            for status in self.content_delivery_lesson_statuses.split(",")
            if status.strip()
        ]

    @property
    def content_tracks(self) -> list[str]:
        return [
            track.strip().lower()
            for track in self.valid_content_tracks.split(",")
            if track.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
