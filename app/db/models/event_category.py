from __future__ import annotations

from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EventSection(str, Enum):
    IMPORTANT = "important"
    AI_NEWS = "ai_news"
    CODING = "coding"
    INVESTMENTS = "investments"
    ALPHA = "alpha"


class EventCategory(Base):
    __tablename__ = "event_categories"
    __table_args__ = (
        UniqueConstraint("event_id", "section", name="uq_event_categories_event_section"),
        Index("ix_event_categories_section", "section"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    section: Mapped[EventSection] = mapped_column(
        SqlEnum(EventSection, name="event_section_enum", values_callable=lambda enum: [i.value for i in enum]),
        nullable=False,
    )
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_primary_section: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    event = relationship("Event", back_populates="categories")
