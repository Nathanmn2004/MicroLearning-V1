from datetime import UTC, datetime


async def health_task(ctx: dict) -> dict[str, str]:
    return {
        "status": "ok",
        "checked_at": datetime.now(UTC).isoformat(),
    }
