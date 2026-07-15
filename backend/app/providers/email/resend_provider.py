from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class ResendConfigurationError(RuntimeError):
    pass


class ResendSendError(RuntimeError):
    pass


class ResendEmailProvider:
    api_url = "https://api.resend.com/emails"

    def __init__(self, api_key: str | None = None, from_email: str | None = None) -> None:
        self.api_key = api_key or settings.resend_api_key
        self.from_email = from_email or settings.resend_from_email

        if not self.api_key:
            raise ResendConfigurationError("RESEND_API_KEY is not configured")
        if not self.from_email:
            raise ResendConfigurationError("RESEND_FROM_EMAIL is not configured")

    def send_email(
        self,
        *,
        to: str | list[str],
        subject: str,
        html: str,
        text: str | None = None,
        tags: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "from": self.from_email,
            "to": [to] if isinstance(to, str) else to,
            "subject": subject,
            "html": html,
        }
        if text is not None:
            payload["text"] = text
        if tags:
            payload["tags"] = tags

        response = httpx.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        if response.status_code >= 400:
            raise ResendSendError(
                f"Resend returned {response.status_code}: {response.text}"
            )
        return response.json()
