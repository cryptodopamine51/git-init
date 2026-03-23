from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SourceType(str, Enum):
    RSS_FEED = "rss_feed"
    WEBSITE = "website"
    OFFICIAL_BLOG = "official_blog"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_type: Mapped[SourceType] = mapped_column(
        SqlEnum(SourceType, name="source_type_enum", values_callable=lambda enum: [i.value for i in enum]),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    handle_or_url: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    priority_weight: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country_scope: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    raw_items = relationship("RawItem", back_populates="source", cascade="all, delete-orphan")
    source_runs = relationship("SourceRun", back_populates="source", cascade="all, delete-orphan")
