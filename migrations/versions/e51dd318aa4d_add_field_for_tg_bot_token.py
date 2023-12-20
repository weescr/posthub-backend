"""add field for tg_bot_token

Revision ID: e51dd318aa4d
Revises: f337b82294b1
Create Date: 2023-12-20 20:43:37.964974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e51dd318aa4d'
down_revision: Union[str, None] = 'f337b82294b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tg_bot_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'tg_bot_token')
    # ### end Alembic commands ###