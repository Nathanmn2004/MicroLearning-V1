from datetime import UTC, datetime

from app.services.content_scheduler import ContentScheduler


async def health_task(ctx: dict) -> dict[str, str]:
    return {
        "status": "ok",
        "checked_at": datetime.now(UTC).isoformat(),
    }


async def run_content_delivery_cycle(ctx: dict) -> dict:
    return ContentScheduler().run_cycle(scheduled_at=datetime.now(UTC))
