"""Add Vietnamese translation columns

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("discourses", sa.Column("title_vi", sa.Text(), nullable=True))
    op.add_column("discourses", sa.Column("full_text_vi", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("discourses", "full_text_vi")
    op.drop_column("discourses", "title_vi")
