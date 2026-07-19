from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from arq.connections import RedisSettings
from arq.cron import cron

from app.core.config import settings
from app.services.content_scheduler import parse_delivery_time
from app.workers.tasks import health_task, run_content_delivery_cycle


def redis_settings_from_url(redis_url: str) -> RedisSettings:
    if redis_url.startswith("redis://"):
        redis_url = redis_url.removeprefix("redis://")
    host_port, _, database = redis_url.partition("/")
    host, _, port = host_port.partition(":")
    return RedisSettings(
        host=host or "localhost",
        port=int(port or 6379),
        database=int(database or 0),
    )


def delivery_cron_utc() -> tuple[int, int]:
    local_zone = ZoneInfo(settings.content_delivery_timezone)
    delivery_time = parse_delivery_time(settings.content_delivery_time)
    local_run_at = datetime.combine(
        datetime.now(local_zone).date(),
        delivery_time,
        tzinfo=local_zone,
    )
    utc_run_at = local_run_at.astimezone(UTC)
    return utc_run_at.hour, utc_run_at.minute


delivery_cron_hour, delivery_cron_minute = delivery_cron_utc()


class WorkerSettings:
    functions = [health_task, run_content_delivery_cycle]
    cron_jobs = [
        cron(
            run_content_delivery_cycle,
            hour=delivery_cron_hour,
            minute=delivery_cron_minute,
        )
    ]
    redis_settings = redis_settings_from_url(settings.redis_url)
