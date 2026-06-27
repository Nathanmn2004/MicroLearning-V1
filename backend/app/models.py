from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        order_by="Lesson.day_number",
    )


class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = (UniqueConstraint("book_id", "day_number", name="uq_lesson_book_day"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False, index=True)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    key_insight: Mapped[str] = mapped_column(Text, nullable=False)
    reflection_question: Mapped[str] = mapped_column(Text, nullable=False)
    source_pages: Mapped[str | None] = mapped_column(String(100), nullable=True)

    book: Mapped[Book] = relationship(back_populates="lessons")
    email_logs: Mapped[list["EmailLog"]] = relationship(back_populates="lesson")


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    subscribed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    confirm_token: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    unsubscribe_token: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)

    email_logs: Mapped[list["EmailLog"]] = relationship(
        back_populates="subscriber",
        cascade="all, delete-orphan",
    )


class EmailLog(Base):
    __tablename__ = "email_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("subscribers.id"), nullable=False, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False, index=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    subscriber: Mapped[Subscriber] = relationship(back_populates="email_logs")
    lesson: Mapped[Lesson] = relationship(back_populates="email_logs")
