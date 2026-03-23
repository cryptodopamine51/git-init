from __future__ import annotations

from enum import Enum

from sqlalchemy import Enum as SqlEnum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EventTagType(str, Enum):
    THEME = "theme"
    ENTITY = "entity"
    MARKET = "market"
    TECH = "tech"


class EventTag(Base):
    __tablename__ = "event_tags"
    __table_args__ = (
        UniqueConstraint("event_id", "tag", "tag_type", name="uq_event_tags_event_tag_type"),
        Index("ix_event_tags_tag", "tag"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    tag: Mapped[str] = mapped_column(String(120), nullable=False)
    tag_type: Mapped[EventTagType] = mapped_column(
        SqlEnum(EventTagType, name="event_tag_type_enum", values_callable=lambda enum: [i.value for i in enum]),
        nullable=False,
    )

    event = relationship("Event", back_populates="tags")
