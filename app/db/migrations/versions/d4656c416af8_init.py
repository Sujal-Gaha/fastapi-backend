"""init

Revision ID: d4656c416af8
Revises:
Create Date: 2026-03-13 11:44:04.742561

"""

import enum
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "d4656c416af8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class TodoPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "todos",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column(
            "user_id",
            sa.String(),
            sa.ForeignKey("users.id"),
            nullable=False,
            index=True,
        ),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("description", sa.String(250), nullable=False),
        sa.Column(
            "priority",
            sa.Enum(TodoPriorityEnum, name="todo_priority_enum"),
            nullable=False,
            server_default="LOW",
            index=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("todos")
    todo_priority = sa.Enum(TodoPriorityEnum, name="todo_priority_enum")
    todo_priority.drop(op.get_bind(), checkfirst=True)
    op.drop_table("users")
