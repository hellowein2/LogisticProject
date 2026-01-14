"""add public_id to parcels

Revision ID: cc14c93fed66
Revises: 4b4e2de35d7c
Create Date: 2026-01-12 17:19:01.084380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision: str = 'cc14c93fed66'
down_revision: Union[str, Sequence[str], None] = '4b4e2de35d7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "parcels",
        sa.Column("public_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id FROM parcels WHERE public_id IS NULL")).fetchall()
    for (parcel_id,) in rows:
        conn.execute(
            sa.text("UPDATE parcels SET public_id = :uid WHERE id = :id"),
            {"uid": str(uuid.uuid4()), "id": parcel_id},
        )

    op.alter_column("parcels", "public_id", nullable=False)
    op.create_unique_constraint("uq_parcels_public_id", "parcels", ["public_id"])


def downgrade():
    op.drop_constraint("uq_parcels_public_id", "parcels", type_="unique")
    op.drop_column("parcels", "public_id")