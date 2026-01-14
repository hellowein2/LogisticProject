"""seed parcel types

Revision ID: 4b4e2de35d7c
Revises: 1c0ab0dacf47
Create Date: 2025-12-29 16:58:47.208186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b4e2de35d7c'
down_revision: Union[str, Sequence[str], None] = '1c0ab0dacf47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    parcel_types_table = sa.table(
        'parcel_types',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
    )

    op.bulk_insert(
        parcel_types_table,
        [
            {'id': 1, 'name': 'Clothes'},
            {'id': 2, 'name': 'Electronics'},
            {'id': 3, 'name': 'Others'},
            ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM parcel_types WHERE name IN ('clothes','electronics','other')")
