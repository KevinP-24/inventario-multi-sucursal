"""crear ordenes compra y detalles

Revision ID: 11d2e3f4a5b6
Revises: 10c1d2e3f4a5
Create Date: 2026-04-10 01:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "11d2e3f4a5b6"
down_revision = "10c1d2e3f4a5"
branch_labels = None
depends_on = None


def upgrade():
    # Cabecera de la compra, alineada al DER.
    op.create_table(
        "orden_compra",
        sa.Column("id_orden_compra", sa.Integer(), nullable=False),
        sa.Column("id_proveedor", sa.Integer(), nullable=False),
        sa.Column("id_sucursal", sa.Integer(), nullable=False),
        sa.Column("id_usuario", sa.Integer(), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("estado", sa.String(length=40), nullable=False),
        sa.Column("plazo_pago", sa.String(length=80), nullable=True),
        sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("descuento_total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("fecha_recepcion", sa.Date(), nullable=True),
        sa.Column("id_usuario_recepcion", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_proveedor"], ["proveedores.id_proveedor"]),
        sa.ForeignKeyConstraint(["id_sucursal"], ["sucursales.id_sucursal"]),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuarios.id_usuario"]),
        sa.ForeignKeyConstraint(["id_usuario_recepcion"], ["usuarios.id_usuario"]),
        sa.PrimaryKeyConstraint("id_orden_compra"),
    )

    # Detalle de productos comprados por orden.
    op.create_table(
        "detalle_orden_compra",
        sa.Column("id_detalle_oc", sa.Integer(), nullable=False),
        sa.Column("id_orden_compra", sa.Integer(), nullable=False),
        sa.Column("id_producto", sa.Integer(), nullable=False),
        sa.Column("id_producto_unidad", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("descuento", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["id_orden_compra"], ["orden_compra.id_orden_compra"]),
        sa.ForeignKeyConstraint(["id_producto"], ["productos.id_producto"]),
        sa.ForeignKeyConstraint(["id_producto_unidad"], ["producto_unidades.id_producto_unidad"]),
        sa.PrimaryKeyConstraint("id_detalle_oc"),
    )


def downgrade():
    op.drop_table("detalle_orden_compra")
    op.drop_table("orden_compra")
