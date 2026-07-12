from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


class SupabaseConfigurationError(RuntimeError):
    pass


def _create_supabase_client(key: str | None) -> Client:
    if not settings.supabase_url:
        raise SupabaseConfigurationError("SUPABASE_URL is not configured")
    if not key:
        raise SupabaseConfigurationError("Supabase API key is not configured")
    return create_client(settings.supabase_url, key)


@lru_cache
def get_supabase_client() -> Client:
    return _create_supabase_client(settings.supabase_anon_key)


@lru_cache
def get_supabase_admin_client() -> Client:
    return _create_supabase_client(settings.supabase_service_role_key)
