from __future__ import annotations

import argparse
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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

from app.providers.email.resend_provider import ResendEmailProvider  # noqa: E402
from app.repositories.supabase_client import get_supabase_admin_client  # noqa: E402
from app.services.email_templates import plain_text, render_lesson_email  # noqa: E402


def sample_lesson() -> dict[str, Any]:
    return {
        "id": "test",
        "title": "Microlicao de teste",
        "content_markdown": (
            "Esta e uma microlicao de teste enviada pelo backend da MicroAprendizagem.\n\n"
            "Se voce recebeu este email, o dominio, a API key e o template estao funcionando."
        ),
        "estimated_reading_minutes": 2,
    }


def get_record(client: Any, table: str, record_id: str) -> dict[str, Any]:
    response = client.table(table).select("*").eq("id", record_id).limit(1).execute()
    if not response.data:
        raise RuntimeError(f"{table} record not found: {record_id}")
    return response.data[0]


def get_first_quote(client: Any, lesson_id: str) -> dict[str, Any] | None:
    response = (
        client.table("lesson_quotes")
        .select("*")
        .eq("lesson_id", lesson_id)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def get_lesson_payload(client: Any, lesson_id: str) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    lesson = get_record(client, "lessons", lesson_id)
    book = get_record(client, "books", lesson["book_id"]) if lesson.get("book_id") else None
    quote = get_first_quote(client, lesson_id)
    return lesson, book, quote


def get_active_subscribers(client: Any, limit: int) -> list[dict[str, Any]]:
    subscriptions = (
        client.table("subscriptions")
        .select("subscriber_id")
        .eq("status", "active")
        .limit(limit)
        .execute()
        .data
    )
    subscriber_ids = {
        row["subscriber_id"]
        for row in subscriptions
        if row.get("subscriber_id")
    }
    subscribers: list[dict[str, Any]] = []
    for subscriber_id in subscriber_ids:
        subscriber = get_record(client, "subscribers", subscriber_id)
        if subscriber.get("email") and subscriber.get("email_enabled", True):
            subscribers.append(subscriber)
    return subscribers


def record_delivery(
    client: Any,
    *,
    lesson_id: str,
    subscriber_id: str,
    provider_message_id: str | None,
) -> None:
    client.table("deliveries").insert(
        {
            "lesson_id": lesson_id,
            "subscriber_id": subscriber_id,
            "channel": "email",
            "status": "sent",
            "sent_at": datetime.now(UTC).isoformat(),
            "provider_message_id": provider_message_id,
        }
    ).execute()


def send_one(
    *,
    provider: ResendEmailProvider,
    to: str,
    subject: str,
    html: str,
    lesson_id: str | None,
) -> dict[str, Any]:
    tags = [{"name": "channel", "value": "email"}]
    if lesson_id:
        tags.append({"name": "lesson_id", "value": lesson_id})
    return provider.send_email(
        to=to,
        subject=subject,
        html=html,
        text=plain_text(html),
        tags=tags,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a lesson email through Resend.")
    parser.add_argument("--to", help="Send a test email to this address.")
    parser.add_argument("--lesson-id", help="Lesson UUID to render and optionally record.")
    parser.add_argument("--subscriber-id", help="Subscriber UUID for delivery registration.")
    parser.add_argument("--active-subscribers", action="store_true", help="Send to active email-enabled subscribers.")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--subject")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-record", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.to and not args.active_subscribers:
        raise RuntimeError("Use --to for a test email or --active-subscribers for subscribers.")
    if args.active_subscribers and not args.lesson_id:
        raise RuntimeError("--active-subscribers requires --lesson-id")

    client = get_supabase_admin_client() if args.lesson_id or args.active_subscribers else None
    if args.lesson_id:
        lesson, book, quote = get_lesson_payload(client, args.lesson_id)
    else:
        lesson, book, quote = sample_lesson(), None, None

    html = render_lesson_email(lesson=lesson, book=book, quote=quote)
    subject = args.subject or f"MicroAprendizagem: {lesson['title']}"

    recipients: list[tuple[str, str | None]] = []
    if args.to:
        recipients.append((args.to, args.subscriber_id))
    if args.active_subscribers:
        recipients.extend(
            (subscriber["email"], subscriber["id"])
            for subscriber in get_active_subscribers(client, args.limit)
        )

    if args.dry_run:
        print(f"Subject: {subject}")
        print(f"Recipients: {len(recipients)}")
        print(html[:1000])
        return

    provider = ResendEmailProvider()
    for email, subscriber_id in recipients:
        result = send_one(
            provider=provider,
            to=email,
            subject=subject,
            html=html,
            lesson_id=args.lesson_id,
        )
        provider_message_id = result.get("id")
        if args.lesson_id and subscriber_id and not args.no_record:
            record_delivery(
                client,
                lesson_id=args.lesson_id,
                subscriber_id=subscriber_id,
                provider_message_id=provider_message_id,
            )
        print(f"Sent to {email}: {provider_message_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise
