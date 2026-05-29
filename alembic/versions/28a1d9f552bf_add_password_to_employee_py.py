"""add_password_to_employee.py

Revision ID: 28a1d9f552bf
Revises: 9b0b68baa6fc
Create Date: 2026-05-29 16:02:54.387640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28a1d9f552bf'
down_revision: Union[str, Sequence[str], None] = '9b0b68baa6fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("employees", sa.Column("password_hash",sa.String(255),nullable=True))
    op.execute("UPDATE employees SET password_hash = 'placeholder' WHERE password_hash IS NULL")
    op.alter_column("employees","password_hash",nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("employees","password_hash",nullable=False)
