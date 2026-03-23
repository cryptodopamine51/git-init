"""slice3 events layer

Revision ID: 20260323_0003
Revises: 20260323_0002
Create Date: 2026-03-23 01:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260323_0003"
down_revision: Union[str, None] = "20260323_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


event_source_role_enum = sa.Enum("primary", "supporting", "reaction", name="event_source_role_enum")
event_section_enum = sa.Enum("important", "ai_news", "coding", "investments", "alpha", name="event_section_enum")
event_tag_type_enum = sa.Enum("theme", "entity", "market", "tech", name="event_tag_type_enum")


def upgrade() -> None:
    op.add_column("sources", sa.Column("meta_json", sa.JSON(), nullable=True))

    event_source_role_enum.create(op.get_bind(), checkfirst=True)
    event_section_enum.create(op.get_bind(), checkfirst=True)
    event_tag_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cluster_key", sa.String(length=512), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("title", sa.String(length=1024), nullable=False),
        sa.Column("short_summary", sa.Text(), nullable=True),
        sa.Column("long_summary", sa.Text(), nullable=True),
        sa.Column("primary_source_id", sa.Integer(), nullable=True),
        sa.Column("primary_source_url", sa.String(length=1024), nullable=True),
        sa.Column("importance_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("market_impact_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("ai_news_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("coding_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("investment_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("is_highlight", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["primary_source_id"], ["sources.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("cluster_key", name="uq_events_cluster_key"),
    )
    op.create_index("ix_events_cluster_key", "events", ["cluster_key"], unique=False)
    op.create_index("ix_events_event_date", "events", ["event_date"], unique=False)
    op.create_index("ix_events_importance_score", "events", ["importance_score"], unique=False)

    op.create_table(
        "event_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("raw_item_id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("role", event_source_role_enum, nullable=False),
        sa.Column("citation_url", sa.String(length=1024), nullable=True),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["raw_item_id"], ["raw_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("event_id", "raw_item_id", name="uq_event_sources_event_raw_item"),
    )
    op.create_index("ix_event_sources_event_id", "event_sources", ["event_id"], unique=False)
    op.create_index("ix_event_sources_source_id", "event_sources", ["source_id"], unique=False)

    op.create_table(
        "event_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("section", event_section_enum, nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("is_primary_section", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("event_id", "section", name="uq_event_categories_event_section"),
    )
    op.create_index("ix_event_categories_section", "event_categories", ["section"], unique=False)

    op.create_table(
        "event_tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("tag", sa.String(length=120), nullable=False),
        sa.Column("tag_type", event_tag_type_enum, nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("event_id", "tag", "tag_type", name="uq_event_tags_event_tag_type"),
    )
    op.create_index("ix_event_tags_tag", "event_tags", ["tag"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_event_tags_tag", table_name="event_tags")
    op.drop_table("event_tags")

    op.drop_index("ix_event_categories_section", table_name="event_categories")
    op.drop_table("event_categories")

    op.drop_index("ix_event_sources_source_id", table_name="event_sources")
    op.drop_index("ix_event_sources_event_id", table_name="event_sources")
    op.drop_table("event_sources")

    op.drop_index("ix_events_importance_score", table_name="events")
    op.drop_index("ix_events_event_date", table_name="events")
    op.drop_index("ix_events_cluster_key", table_name="events")
    op.drop_table("events")

    event_tag_type_enum.drop(op.get_bind(), checkfirst=True)
    event_section_enum.drop(op.get_bind(), checkfirst=True)
    event_source_role_enum.drop(op.get_bind(), checkfirst=True)

    op.drop_column("sources", "meta_json")
