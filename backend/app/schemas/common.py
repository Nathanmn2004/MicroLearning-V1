from enum import StrEnum


class LessonStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    ARCHIVED = "archived"


class SubscriptionStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    REFUNDED = "refunded"
    UNKNOWN = "unknown"


class DeliveryChannel(StrEnum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class DeliveryStatus(StrEnum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"
