"""users_update_2

Revision ID: da70bf412d6c
Revises: 05313e74c53a
Create Date: 2023-11-23 01:17:59.315534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da70bf412d6c'
down_revision: Union[str, None] = '05313e74c53a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True, default="your@example.com"),
        sa.Column('tg_channel', sa.String(), nullable=True, default="@yourtg"),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')