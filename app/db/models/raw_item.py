from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.source import SourceType


class RawItemStatus(str, Enum):
    FETCHED = "fetched"
    NORMALIZED = "normalized"
    CLUSTERED = "clustered"
    DISCARDED = "discarded"


class RawItem(Base):
    __tablename__ = "raw_items"
    __table_args__ = (
        UniqueConstraint("source_id", "external_id", name="uq_raw_items_source_external"),
        Index("ix_raw_items_source_id_published_at", "source_id", "published_at"),
        Index("ix_raw_items_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(String(512), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(
        SqlEnum(SourceType, name="source_type_enum", values_callable=lambda enum: [i.value for i in enum]),
        nullable=False,
    )
    author_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    canonical_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    raw_title: Mapped[str] = mapped_column(String(1024), nullable=False)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[RawItemStatus] = mapped_column(
        SqlEnum(RawItemStatus, name="raw_item_status_enum", values_callable=lambda enum: [i.value for i in enum]),
        default=RawItemStatus.FETCHED,
        nullable=False,
    )
    normalized_title: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    normalized_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    entities_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    outbound_links_json: Mapped[list | None] = mapped_column(JSON, nullable=True)

    source = relationship("Source", back_populates="raw_items")
