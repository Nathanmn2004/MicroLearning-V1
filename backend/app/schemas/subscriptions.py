from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import SubscriptionStatus


class SubscriptionCreate(BaseModel):
    subscriber_id: UUID | None = None
    provider: str = "cakto"
    provider_customer_id: str | None = None
    provider_subscription_id: str | None = None
    plan_name: str | None = None
    status: SubscriptionStatus = SubscriptionStatus.UNKNOWN


class SubscriptionUpdate(BaseModel):
    provider_customer_id: str | None = None
    provider_subscription_id: str | None = None
    plan_name: str | None = None
    status: SubscriptionStatus | None = None
    started_at: datetime | None = None
    current_period_end: datetime | None = None
    cancelled_at: datetime | None = None
    last_verified_at: datetime | None = None


class SubscriptionRead(SubscriptionCreate):
    id: UUID
    started_at: datetime | None = None
    current_period_end: datetime | None = None
    cancelled_at: datetime | None = None
    last_verified_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
