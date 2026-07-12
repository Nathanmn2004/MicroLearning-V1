from arq.connections import RedisSettings

from app.core.config import settings
from app.workers.tasks import health_task


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


class WorkerSettings:
    functions = [health_task]
    redis_settings = redis_settings_from_url(settings.redis_url)
