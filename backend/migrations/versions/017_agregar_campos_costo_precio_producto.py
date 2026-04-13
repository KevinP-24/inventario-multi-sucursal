"""agregar campos de costo y precio a productos

Revision ID: 17d8e9f0a1b2
Revises: 16c7d8e9f0a1
Create Date: 2026-04-13 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "17d8e9f0a1b2"
down_revision = "16c7d8e9f0a1"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("productos", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("ultimo_costo_compra", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0")
        )
        batch_op.add_column( sa.Column("precio_venta_base", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0")
        )


def downgrade():
    with op.batch_alter_table("productos", schema=None) as batch_op:
        batch_op.drop_column("precio_venta_base")
        batch_op.drop_column("ultimo_costo_compra")
