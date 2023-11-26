"""updated_tables

Revision ID: 0cc128775b71
Revises: ef1e20c54e7f
Create Date: 2023-11-26 18:01:13.924241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cc128775b71'
down_revision: Union[str, None] = 'ef1e20c54e7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
