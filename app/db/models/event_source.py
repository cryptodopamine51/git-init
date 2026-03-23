from __future__ import annotations

from enum import Enum

from sqlalchemy import Enum as SqlEnum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EventSourceRole(str, Enum):
    PRIMARY = "primary"
    SUPPORTING = "supporting"
    REACTION = "reaction"


class EventSource(Base):
    __tablename__ = "event_sources"
    __table_args__ = (
        UniqueConstraint("event_id", "raw_item_id", name="uq_event_sources_event_raw_item"),
        Index("ix_event_sources_event_id", "event_id"),
        Index("ix_event_sources_source_id", "source_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    raw_item_id: Mapped[int] = mapped_column(ForeignKey("raw_items.id", ondelete="CASCADE"), nullable=False)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[EventSourceRole] = mapped_column(
        SqlEnum(EventSourceRole, name="event_source_role_enum", values_callable=lambda enum: [i.value for i in enum]),
        nullable=False,
    )
    citation_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    event = relationship("Event", back_populates="sources")
