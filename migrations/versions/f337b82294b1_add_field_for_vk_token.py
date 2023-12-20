"""add field for vk_token

Revision ID: f337b82294b1
Revises: 1700707f3f0e
Create Date: 2023-12-20 20:20:05.818278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f337b82294b1'
down_revision: Union[str, None] = '1700707f3f0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('vk_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'vk_token')
    # ### end Alembic commands ###