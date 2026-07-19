from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BookBase(BaseModel):
    slug: str
    title: str
    author: str | None = None
    description: str | None = None
    category: str | None = None
    content_track: str = "todos"
    language: str = "pt-BR"
    file_path: str
    enabled: bool = True


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    category: str | None = None
    content_track: str | None = None
    language: str | None = None
    file_path: str | None = None
    page_count: int | None = None
    enabled: bool | None = None


class BookRead(BookBase):
    id: UUID
    page_count: int | None = None
    processing_version: int
    processed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
