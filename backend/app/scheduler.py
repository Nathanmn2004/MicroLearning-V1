from datetime import date

from sqlalchemy import func

from .config import get_settings
from .database import SessionLocal
from .email_service import send_daily_lesson_email
from .models import EmailLog, Lesson, Subscriber

settings = get_settings()

try:
    from apscheduler.schedulers.background import BackgroundScheduler
except ImportError:
    BackgroundScheduler = None

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo") if BackgroundScheduler else None


def get_lesson_for_today(db) -> Lesson | None:
    total_lessons = db.query(func.count(Lesson.id)).scalar() or 0
    if total_lessons == 0:
        return None

    epoch = date.fromisoformat(settings.content_epoch)
    day_number = ((date.today() - epoch).days % total_lessons) + 1
    return db.query(Lesson).order_by(Lesson.day_number).offset(day_number - 1).first()


def run_daily_job() -> None:
    db = SessionLocal()
    try:
        lesson = get_lesson_for_today(db)
        if lesson is None:
            print("[scheduler] No lessons available.")
            return

        subscribers = db.query(Subscriber).filter(Subscriber.confirmed.is_(True)).all()
        for subscriber in subscribers:
            status = "sent"
            try:
                send_daily_lesson_email(subscriber, lesson)
            except Exception as exc:
                status = f"failed: {exc}"

            db.add(EmailLog(subscriber_id=subscriber.id, lesson_id=lesson.id, status=status[:50]))
            db.commit()
    finally:
        db.close()


def start_scheduler() -> None:
    if scheduler is None:
        print("[scheduler] APScheduler is not installed; daily job is disabled.")
        return

    if scheduler.running:
        return

    scheduler.add_job(
        run_daily_job,
        "cron",
        hour=settings.send_hour,
        minute=settings.send_minute,
        id="daily_lesson_email",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler is not None and scheduler.running:
        scheduler.shutdown()
