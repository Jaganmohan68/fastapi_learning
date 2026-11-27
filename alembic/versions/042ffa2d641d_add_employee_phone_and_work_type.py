"""add employee phone and work type

Revision ID: 042ffa2d641d
Revises: c210649e53db
Create Date: 2026-11-27 11:34:56.883262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '042ffa2d641d'
down_revision: Union[str, Sequence[str], None] = 'c210649e53db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add employee phone number and work arrangement columns."""
    op.add_column(
        "employees",
        sa.Column("phone_number", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "employees",
        sa.Column("work_type", sa.String(length=30), nullable=True),
    )
    op.create_check_constraint(
        "ck_employees_work_type",
        "employees",
        "work_type IS NULL OR work_type IN ('remote', 'work_from_office')",
    )


def downgrade() -> None:
    """Remove employee work arrangement and phone number columns."""
    op.drop_constraint("ck_employees_work_type", "employees", type_="check")
    op.drop_column("employees", "work_type")
    op.drop_column("employees", "phone_number")
