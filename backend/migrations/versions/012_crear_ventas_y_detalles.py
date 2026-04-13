"""crear ventas y detalles

Revision ID: 12e3f4a5b6c7
Revises: 11d2e3f4a5b6
Create Date: 2026-04-10 02:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "12e3f4a5b6c7"
down_revision = "11d2e3f4a5b6"
branch_labels = None
depends_on = None


def upgrade():
    # Cabecera de la venta, alineada al DER y al flujo de venta documentado.
    op.create_table(
        "venta",
        sa.Column("id_venta", sa.Integer(), nullable=False),
        sa.Column("id_sucursal", sa.Integer(), nullable=False),
        sa.Column("id_usuario", sa.Integer(), nullable=False),
        sa.Column("id_cliente", sa.Integer(), nullable=True),
        sa.Column("id_lista_precio", sa.Integer(), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.Column("descuento_total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("comprobante", sa.String(length=80), nullable=False),
        sa.Column("estado", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["id_sucursal"], ["sucursales.id_sucursal"]),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuarios.id_usuario"]),
        sa.ForeignKeyConstraint(["id_cliente"], ["clientes.id_cliente"]),
        sa.ForeignKeyConstraint(["id_lista_precio"], ["listas_precio.id_lista_precio"]),
        sa.PrimaryKeyConstraint("id_venta"),
    )

    # Detalle de productos vendidos. El precio unitario queda congelado aqui.
    op.create_table(
        "detalle_venta",
        sa.Column("id_detalle_venta", sa.Integer(), nullable=False),
        sa.Column("id_venta", sa.Integer(), nullable=False),
        sa.Column("id_producto", sa.Integer(), nullable=False),
        sa.Column("id_producto_unidad", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("descuento", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["id_venta"], ["venta.id_venta"]),
        sa.ForeignKeyConstraint(["id_producto"], ["productos.id_producto"]),
        sa.ForeignKeyConstraint(["id_producto_unidad"], ["producto_unidades.id_producto_unidad"]),
        sa.PrimaryKeyConstraint("id_detalle_venta"),
    )


def downgrade():
    op.drop_table("detalle_venta")
    op.drop_table("venta")
