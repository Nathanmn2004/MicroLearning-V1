from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, time, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from app.core.config import settings
from app.providers.email.resend_provider import (
    ResendConfigurationError,
    ResendEmailProvider,
)
from app.repositories.supabase_client import get_supabase_admin_client
from app.services.email_templates import plain_text, render_lesson_email


TERMINAL_DELIVERY_STATUSES = {"sent", "delivered"}
BLOCKING_DELIVERY_STATUSES = {
    "pending",
    "scheduled",
    "sending",
    *TERMINAL_DELIVERY_STATUSES,
}


@dataclass
class ScheduleResult:
    subscribers_checked: int = 0
    lessons_available: int = 0
    scheduled: int = 0
    skipped_no_channel: int = 0
    skipped_no_lesson: int = 0
    skipped_whatsapp_unavailable: int = 0
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "subscribers_checked": self.subscribers_checked,
            "lessons_available": self.lessons_available,
            "scheduled": self.scheduled,
            "skipped_no_channel": self.skipped_no_channel,
            "skipped_no_lesson": self.skipped_no_lesson,
            "skipped_whatsapp_unavailable": self.skipped_whatsapp_unavailable,
            "errors": self.errors,
        }


@dataclass
class SendResult:
    checked: int = 0
    sent: int = 0
    failed: int = 0
    dry_run: bool = False
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "checked": self.checked,
            "sent": self.sent,
            "failed": self.failed,
            "dry_run": self.dry_run,
            "errors": self.errors,
        }


def parse_delivery_time(value: str) -> time:
    hour_text, _, minute_text = value.partition(":")
    if not hour_text or not minute_text:
        raise ValueError("CONTENT_DELIVERY_TIME must use HH:MM format")
    return time(hour=int(hour_text), minute=int(minute_text))


def next_scheduled_at_utc(now: datetime | None = None) -> datetime:
    local_zone = ZoneInfo(settings.content_delivery_timezone)
    local_now = (now or datetime.now(UTC)).astimezone(local_zone)
    delivery_time = parse_delivery_time(settings.content_delivery_time)
    candidate = datetime.combine(local_now.date(), delivery_time, tzinfo=local_zone)

    frequency = settings.content_delivery_frequency.lower()
    if frequency == "daily":
        if candidate <= local_now:
            candidate += timedelta(days=1)
    elif frequency == "weekdays":
        if candidate <= local_now:
            candidate += timedelta(days=1)
        while candidate.weekday() >= 5:
            candidate += timedelta(days=1)
    elif frequency == "weekly":
        if candidate <= local_now:
            candidate += timedelta(days=7)
    else:
        raise ValueError(
            "CONTENT_DELIVERY_FREQUENCY must be daily, weekdays, or weekly"
        )

    return candidate.astimezone(UTC)


class ContentScheduler:
    def __init__(
        self,
        *,
        client: Any | None = None,
        email_provider: ResendEmailProvider | None = None,
    ) -> None:
        self.client = client or get_supabase_admin_client()
        self.email_provider = email_provider

    def active_subscribers(self, limit: int) -> list[dict[str, Any]]:
        response = (
            self.client.table("subscriptions")
            .select("subscriber_id")
            .eq("status", "active")
            .limit(limit)
            .execute()
        )
        subscriber_ids = []
        seen = set()
        for row in response.data or []:
            subscriber_id = row.get("subscriber_id")
            if subscriber_id and subscriber_id not in seen:
                seen.add(subscriber_id)
                subscriber_ids.append(subscriber_id)

        subscribers: list[dict[str, Any]] = []
        for subscriber_id in subscriber_ids:
            subscriber = self.get_record("subscribers", subscriber_id)
            if subscriber:
                subscribers.append(subscriber)
        return subscribers

    def eligible_lessons(self, limit: int = 1000) -> list[dict[str, Any]]:
        response = (
            self.client.table("lessons")
            .select("*")
            .in_("status", settings.delivery_lesson_statuses)
            .order("created_at")
            .limit(limit)
            .execute()
        )
        return response.data or []

    def get_record(self, table: str, record_id: str) -> dict[str, Any] | None:
        response = (
            self.client.table(table)
            .select("*")
            .eq("id", record_id)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    def subscriber_channels(
        self,
        subscriber: dict[str, Any],
        requested_channels: list[str],
    ) -> list[str]:
        preferred = (subscriber.get("preferred_channel") or "both").lower()
        channels: list[str] = []
        if (
            "email" in requested_channels
            and subscriber.get("email")
            and subscriber.get("email_enabled", True)
            and preferred in {"both", "email"}
        ):
            channels.append("email")
        if (
            "whatsapp" in requested_channels
            and subscriber.get("phone")
            and subscriber.get("whatsapp_enabled", True)
            and preferred in {"both", "whatsapp"}
        ):
            channels.append("whatsapp")
        return channels

    def delivered_lesson_ids(self, subscriber_id: str, channel: str) -> set[str]:
        response = (
            self.client.table("deliveries")
            .select("lesson_id,status")
            .eq("subscriber_id", subscriber_id)
            .eq("channel", channel)
            .execute()
        )
        return {
            row["lesson_id"]
            for row in response.data or []
            if row.get("status") in BLOCKING_DELIVERY_STATUSES and row.get("lesson_id")
        }

    def next_lesson_for(
        self,
        *,
        subscriber: dict[str, Any],
        subscriber_id: str,
        channel: str,
        eligible_lessons: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        blocked_lesson_ids = self.delivered_lesson_ids(subscriber_id, channel)
        subscriber_track = subscriber.get("content_track") or "todos"
        for lesson in eligible_lessons:
            lesson_track = lesson.get("content_track") or "todos"
            if subscriber_track != "todos" and lesson_track != subscriber_track:
                continue
            if lesson["id"] not in blocked_lesson_ids:
                return lesson
        return None

    def schedule_next_lessons(
        self,
        *,
        channels: list[str] | None = None,
        limit: int | None = None,
        scheduled_at: datetime | None = None,
        dry_run: bool = False,
    ) -> ScheduleResult:
        requested_channels = channels or settings.delivery_channels
        batch_limit = limit or settings.content_delivery_batch_limit
        result = ScheduleResult()
        subscribers = self.active_subscribers(batch_limit)
        lessons = self.eligible_lessons()
        result.subscribers_checked = len(subscribers)
        result.lessons_available = len(lessons)

        if not lessons:
            result.skipped_no_lesson = len(subscribers)
            return result

        delivery_time = scheduled_at or next_scheduled_at_utc()
        for subscriber in subscribers:
            subscriber_id = subscriber["id"]
            channels_for_subscriber = self.subscriber_channels(
                subscriber,
                requested_channels,
            )
            if not channels_for_subscriber:
                result.skipped_no_channel += 1
                continue

            for channel in channels_for_subscriber:
                if channel == "whatsapp":
                    result.skipped_whatsapp_unavailable += 1
                    continue

                lesson = self.next_lesson_for(
                    subscriber=subscriber,
                    subscriber_id=subscriber_id,
                    channel=channel,
                    eligible_lessons=lessons,
                )
                if not lesson:
                    result.skipped_no_lesson += 1
                    continue

                if dry_run:
                    result.scheduled += 1
                    continue

                try:
                    self.client.table("deliveries").insert(
                        {
                            "lesson_id": lesson["id"],
                            "subscriber_id": subscriber_id,
                            "channel": channel,
                            "status": "scheduled",
                            "scheduled_at": delivery_time.isoformat(),
                        }
                    ).execute()
                    result.scheduled += 1
                except Exception as exc:
                    result.errors.append(
                        f"{subscriber_id}:{lesson['id']}:{channel}:{exc.__class__.__name__}"
                    )
        return result

    def due_deliveries(
        self,
        *,
        channel: str = "email",
        limit: int | None = None,
        now: datetime | None = None,
    ) -> list[dict[str, Any]]:
        due_at = (now or datetime.now(UTC)).isoformat()
        response = (
            self.client.table("deliveries")
            .select("*")
            .eq("channel", channel)
            .in_("status", ["pending", "scheduled"])
            .lte("scheduled_at", due_at)
            .order("scheduled_at")
            .limit(limit or settings.content_delivery_batch_limit)
            .execute()
        )
        return response.data or []

    def first_quote(self, lesson_id: str) -> dict[str, Any] | None:
        response = (
            self.client.table("lesson_quotes")
            .select("*")
            .eq("lesson_id", lesson_id)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    def mark_delivery(
        self,
        delivery_id: str,
        data: dict[str, Any],
    ) -> None:
        self.client.table("deliveries").update(data).eq("id", delivery_id).execute()

    def send_due_email_deliveries(
        self,
        *,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> SendResult:
        result = SendResult(dry_run=dry_run)
        deliveries = self.due_deliveries(channel="email", limit=limit)
        result.checked = len(deliveries)
        if dry_run:
            result.sent = len(deliveries)
            return result

        try:
            provider = self.email_provider or ResendEmailProvider()
        except ResendConfigurationError as exc:
            result.failed = len(deliveries)
            result.errors.append(str(exc))
            return result

        for delivery in deliveries:
            delivery_id = delivery["id"]
            now_iso = datetime.now(UTC).isoformat()
            self.mark_delivery(delivery_id, {"status": "sending", "sent_at": now_iso})
            try:
                subscriber = self.get_record("subscribers", delivery["subscriber_id"])
                lesson = self.get_record("lessons", delivery["lesson_id"])
                if not subscriber or not subscriber.get("email"):
                    raise RuntimeError("Subscriber email not available")
                if not lesson:
                    raise RuntimeError("Lesson not found")

                book = (
                    self.get_record("books", lesson["book_id"])
                    if lesson.get("book_id")
                    else None
                )
                quote = self.first_quote(lesson["id"])
                html = render_lesson_email(lesson=lesson, book=book, quote=quote)
                response = provider.send_email(
                    to=subscriber["email"],
                    subject=f"MicroAprendizagem: {lesson['title']}",
                    html=html,
                    text=plain_text(html),
                    tags=[
                        {"name": "channel", "value": "email"},
                        {"name": "lesson_id", "value": lesson["id"]},
                    ],
                )
                self.mark_delivery(
                    delivery_id,
                    {
                        "status": "sent",
                        "sent_at": datetime.now(UTC).isoformat(),
                        "provider_message_id": response.get("id"),
                        "error_message": None,
                    },
                )
                result.sent += 1
            except Exception as exc:
                self.mark_delivery(
                    delivery_id,
                    {
                        "status": "failed",
                        "error_message": str(exc)[:1000],
                        "retry_count": int(delivery.get("retry_count") or 0) + 1,
                    },
                )
                result.failed += 1
                result.errors.append(f"{delivery_id}:{exc.__class__.__name__}")
        return result

    def run_cycle(
        self,
        *,
        channels: list[str] | None = None,
        limit: int | None = None,
        scheduled_at: datetime | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        schedule_result = self.schedule_next_lessons(
            channels=channels,
            limit=limit,
            scheduled_at=scheduled_at,
            dry_run=dry_run,
        )
        send_result = self.send_due_email_deliveries(limit=limit, dry_run=dry_run)
        return {
            "schedule": schedule_result.as_dict(),
            "send": send_result.as_dict(),
        }
