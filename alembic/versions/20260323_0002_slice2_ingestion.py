"""slice2 ingestion foundation

Revision ID: 20260323_0002
Revises: 20260323_0001
Create Date: 2026-03-23 00:30:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260323_0002"
down_revision: Union[str, None] = "20260323_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


source_type_enum = sa.Enum("rss_feed", "website", "official_blog", name="source_type_enum")
raw_item_status_enum = sa.Enum("fetched", "normalized", "clustered", "discarded", name="raw_item_status_enum")
source_run_status_enum = sa.Enum("success", "partial", "failed", name="source_run_status_enum")


def upgrade() -> None:
    source_type_enum.create(op.get_bind(), checkfirst=True)
    raw_item_status_enum.create(op.get_bind(), checkfirst=True)
    source_run_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_type", source_type_enum, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("handle_or_url", sa.String(length=1024), nullable=False),
        sa.Column("priority_weight", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("language", sa.String(length=20), nullable=True),
        sa.Column("country_scope", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("handle_or_url", name="uq_sources_handle_or_url"),
    )
    op.create_index("ix_sources_source_type", "sources", ["source_type"], unique=False)
    op.create_index("ix_sources_is_active", "sources", ["is_active"], unique=False)

    op.create_table(
        "raw_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=512), nullable=False),
        sa.Column("source_type", source_type_enum, nullable=False),
        sa.Column("author_name", sa.String(length=255), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("canonical_url", sa.String(length=1024), nullable=False),
        sa.Column("raw_title", sa.String(length=1024), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("raw_payload_json", sa.JSON(), nullable=False),
        sa.Column("language", sa.String(length=20), nullable=True),
        sa.Column("status", raw_item_status_enum, nullable=False, server_default="fetched"),
        sa.Column("normalized_title", sa.String(length=1024), nullable=True),
        sa.Column("normalized_text", sa.Text(), nullable=True),
        sa.Column("entities_json", sa.JSON(), nullable=True),
        sa.Column("outbound_links_json", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("source_id", "external_id", name="uq_raw_items_source_external"),
    )
    op.create_index("ix_raw_items_source_id", "raw_items", ["source_id"], unique=False)
    op.create_index("ix_raw_items_published_at", "raw_items", ["published_at"], unique=False)
    op.create_index("ix_raw_items_status", "raw_items", ["status"], unique=False)
    op.create_index("ix_raw_items_source_id_published_at", "raw_items", ["source_id", "published_at"], unique=False)

    op.create_table(
        "source_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", source_run_status_enum, nullable=False, server_default="success"),
        sa.Column("fetched_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("inserted_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_source_runs_source_id", "source_runs", ["source_id"], unique=False)
    op.create_index("ix_source_runs_status", "source_runs", ["status"], unique=False)
    op.create_index("ix_source_runs_source_started", "source_runs", ["source_id", "started_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_source_runs_source_started", table_name="source_runs")
    op.drop_index("ix_source_runs_status", table_name="source_runs")
    op.drop_index("ix_source_runs_source_id", table_name="source_runs")
    op.drop_table("source_runs")

    op.drop_index("ix_raw_items_source_id_published_at", table_name="raw_items")
    op.drop_index("ix_raw_items_status", table_name="raw_items")
    op.drop_index("ix_raw_items_published_at", table_name="raw_items")
    op.drop_index("ix_raw_items_source_id", table_name="raw_items")
    op.drop_table("raw_items")

    op.drop_index("ix_sources_is_active", table_name="sources")
    op.drop_index("ix_sources_source_type", table_name="sources")
    op.drop_table("sources")

    source_run_status_enum.drop(op.get_bind(), checkfirst=True)
    raw_item_status_enum.drop(op.get_bind(), checkfirst=True)
    source_type_enum.drop(op.get_bind(), checkfirst=True)
