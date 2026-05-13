"""add agent_logs table

Revision ID: af92b31e2ef2
Revises: a96f1d219fea
Create Date: 2026-05-13 20:45:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "af92b31e2ef2"
down_revision: Union[str, Sequence[str], None] = "a96f1d219fea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agent_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("normalized_query", sa.Text(), nullable=False),
        sa.Column("plan", sa.Text(), nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_logs_id"), "agent_logs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_agent_logs_id"), table_name="agent_logs")
    op.drop_table("agent_logs")
