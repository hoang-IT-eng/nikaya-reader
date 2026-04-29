"""Initial schema

Revision ID: 0001
Revises: 
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # discourses table
    op.create_table(
        "discourses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mn_number", sa.Integer(), nullable=False, unique=True),
        sa.Column("title_en", sa.Text(), nullable=False),
        sa.Column("title_pali", sa.Text()),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("vagga", sa.Text()),
        sa.Column("page_start", sa.Integer()),
        sa.Column("page_end", sa.Integer()),
        sa.Column("full_text", sa.Text()),
    )
    op.execute(
        "CREATE INDEX ix_discourses_trgm ON discourses "
        "USING GIN (full_text gin_trgm_ops)"
    )

    # chunks table
    op.create_table(
        "chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("discourse_id", sa.Integer(), sa.ForeignKey("discourses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("embedding", sa.Text()),  # stored as text until pgvector type is available
    )

    # bookmarks table
    op.create_table(
        "bookmarks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mn_number", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), server_default=""),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("bookmarks")
    op.drop_table("chunks")
    op.drop_table("discourses")
