from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubscriberCreate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    preferred_channel: str = "both"
    whatsapp_enabled: bool = True
    email_enabled: bool = True
    content_track: str = "todos"
    source: str = "cakto"
    provider_customer_id: str | None = None


class SubscriberUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    preferred_channel: str | None = None
    whatsapp_enabled: bool | None = None
    email_enabled: bool | None = None
    content_track: str | None = None
    provider_customer_id: str | None = None


class SubscriberRead(SubscriberCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
