from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import DeliveryChannel, DeliveryStatus


class DeliveryCreate(BaseModel):
    lesson_id: UUID
    subscriber_id: UUID | None = None
    channel: DeliveryChannel
    scheduled_at: datetime | None = None


class DeliveryUpdate(BaseModel):
    status: DeliveryStatus | None = None
    scheduled_at: datetime | None = None
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    provider_message_id: str | None = None
    error_message: str | None = None
    retry_count: int | None = None


class DeliveryRead(DeliveryCreate):
    id: UUID
    status: DeliveryStatus
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    provider_message_id: str | None = None
    error_message: str | None = None
    retry_count: int
    created_at: datetime
    updated_at: datetime
