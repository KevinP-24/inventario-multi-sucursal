"""crear inventario sucursal

Revision ID: 8a6d1b2c3e4f
Revises: 7f2b83d6c1a4
Create Date: 2026-04-10 00:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8a6d1b2c3e4f"
down_revision = "7f2b83d6c1a4"
branch_labels = None
depends_on = None


def upgrade():
    # Stock actual por producto en cada sucursal, tal como esta en el DER.
    op.create_table(
        "inventario_sucursal",
        sa.Column("id_inventario", sa.Integer(), nullable=False),
        sa.Column("id_sucursal", sa.Integer(), nullable=False),
        sa.Column("id_producto", sa.Integer(), nullable=False),
        sa.Column("cantidad_actual", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("costo_promedio", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["id_producto"], ["productos.id_producto"]),
        sa.ForeignKeyConstraint(["id_sucursal"], ["sucursales.id_sucursal"]),
        sa.PrimaryKeyConstraint("id_inventario"),
        sa.UniqueConstraint("id_sucursal", "id_producto", name="uq_inventario_sucursal_producto"),
    )


def downgrade():
    op.drop_table("inventario_sucursal")
