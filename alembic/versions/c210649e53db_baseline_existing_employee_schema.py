"""baseline existing employee schema

Revision ID: c210649e53db
Revises: 
Create Date: 2026-11-27 11:34:22.916963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c210649e53db'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Describe the employee table as it exists before this migration chain."""
    op.create_table(
        "employees",
        sa.Column("employee_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("department", sa.String(), nullable=False),
        sa.Column("salary", sa.Integer(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("emp_email", sa.String(length=254), nullable=True),
        sa.PrimaryKeyConstraint("employee_id"),
    )
    op.create_index(
        "ix_employees_employee_id", "employees", ["employee_id"], unique=False
    )
    op.create_index(
        "ix_employees_emp_email", "employees", ["emp_email"], unique=True
    )


def downgrade() -> None:
    """Remove the employee table created by the baseline migration."""
    op.drop_index("ix_employees_emp_email", table_name="employees")
    op.drop_index("ix_employees_employee_id", table_name="employees")
    op.drop_table("employees")
