from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from dotenv import dotenv_values


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))


def load_env() -> None:
    for env_path in (ROOT_DIR / ".env", BACKEND_DIR / ".env"):
        values = dotenv_values(env_path)
        for key, value in values.items():
            if value is not None:
                os.environ.setdefault(key, value)


load_env()

from app.core.config import settings  # noqa: E402
from app.services.content_scheduler import ContentScheduler, next_scheduled_at_utc  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Schedule and send recurring MicroAprendizagem lessons."
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=settings.content_delivery_batch_limit)
    parser.add_argument(
        "--channels",
        default=",".join(settings.delivery_channels),
        help="Comma-separated channels. WhatsApp is ignored until etapa 8 exists.",
    )
    parser.add_argument(
        "--schedule-now",
        action="store_true",
        help="Use the current instant instead of CONTENT_DELIVERY_TIME.",
    )
    parser.add_argument(
        "--skip-schedule",
        action="store_true",
        help="Only send due deliveries already in the database.",
    )
    parser.add_argument(
        "--skip-send",
        action="store_true",
        help="Only create scheduled delivery records.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scheduler = ContentScheduler()
    channels = [
        channel.strip().lower()
        for channel in args.channels.split(",")
        if channel.strip()
    ]
    scheduled_at = datetime.now(UTC) if args.schedule_now else next_scheduled_at_utc()

    output: dict[str, object] = {
        "dry_run": args.dry_run,
        "scheduled_at": scheduled_at.isoformat(),
        "channels": channels,
    }
    if not args.skip_schedule:
        output["schedule"] = scheduler.schedule_next_lessons(
            channels=channels,
            limit=args.limit,
            scheduled_at=scheduled_at,
            dry_run=args.dry_run,
        ).as_dict()
    if not args.skip_send:
        output["send"] = scheduler.send_due_email_deliveries(
            limit=args.limit,
            dry_run=args.dry_run,
        ).as_dict()

    print(json.dumps(output, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
