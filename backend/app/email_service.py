from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import get_settings
from .models import Lesson, Subscriber

try:
    import resend
except ImportError:
    resend = None

settings = get_settings()
templates_dir = Path(__file__).parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)


def _send_email(to: str, subject: str, html: str) -> dict:
    if resend is None or not settings.resend_api_key or settings.resend_api_key.startswith("re_..."):
        print(f"[email:dry-run] to={to} subject={subject}")
        return {"id": "dry-run"}

    resend.api_key = settings.resend_api_key
    return resend.Emails.send(
        {
            "from": settings.from_email,
            "to": [to],
            "subject": subject,
            "html": html,
        }
    )


def send_confirmation_email(subscriber: Subscriber) -> dict:
    confirm_url = f"{settings.frontend_url}/confirmed?token={subscriber.confirm_token}"
    html = jinja_env.get_template("confirm_email.html").render(
        subscriber=subscriber,
        confirm_url=confirm_url,
    )
    return _send_email(
        subscriber.email,
        "Confirme sua assinatura de microaprendizagem",
        html,
    )


def send_daily_lesson_email(subscriber: Subscriber, lesson: Lesson) -> dict:
    unsubscribe_url = f"{settings.frontend_url}/unsubscribed?token={subscriber.unsubscribe_token}"
    html = jinja_env.get_template("daily_email.html").render(
        subscriber=subscriber,
        lesson=lesson,
        unsubscribe_url=unsubscribe_url,
    )
    return _send_email(
        subscriber.email,
        f"Sua lição de hoje - {lesson.title}",
        html,
    )
