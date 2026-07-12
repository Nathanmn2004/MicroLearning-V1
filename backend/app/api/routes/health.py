from fastapi import APIRouter

from app.core.config import settings
from app.repositories.health_repository import SupabaseHealthRepository
from app.repositories.supabase_client import SupabaseConfigurationError


router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "version": settings.app_version,
    }


@router.get("/health/supabase")
async def supabase_health_check() -> dict[str, str]:
    try:
        SupabaseHealthRepository().check_connection()
    except SupabaseConfigurationError as exc:
        return {
            "status": "not_configured",
            "detail": str(exc),
        }
    except Exception as exc:
        return {
            "status": "error",
            "detail": exc.__class__.__name__,
        }

    return {
        "status": "ok",
        "service": "supabase",
    }
