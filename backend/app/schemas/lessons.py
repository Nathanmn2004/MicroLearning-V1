from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import LessonStatus


class LessonCreate(BaseModel):
    book_id: UUID
    title: str
    content_track: str = "todos"
    content_markdown: str | None = None
    content_html: str | None = None
    whatsapp_content: str | None = None


class LessonUpdate(BaseModel):
    title: str | None = None
    content_markdown: str | None = None
    content_html: str | None = None
    whatsapp_content: str | None = None
    content_track: str | None = None
    word_count: int | None = None
    estimated_reading_minutes: int | None = None
    status: LessonStatus | None = None


class LessonRead(LessonCreate):
    id: UUID
    word_count: int | None = None
    estimated_reading_minutes: int | None = None
    status: LessonStatus
    version: int
    approved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
