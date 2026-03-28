"""phone number added.

Revision ID: e6fa18b7b723
Revises: 
Create Date: 2026-03-16 13:09:54.101278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6fa18b7b723'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column( "phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    #op.drop_column("users",  "phone_number")
    pass
