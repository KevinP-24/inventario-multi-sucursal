"""crear movimientos inventario

Revision ID: 9b7c6d5e4f30
Revises: 8a6d1b2c3e4f
Create Date: 2026-04-10 00:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9b7c6d5e4f30"
down_revision = "8a6d1b2c3e4f"
branch_labels = None
depends_on = None


def upgrade():
    # Historial de inventario segun el DER. Esta tabla no guarda stock actual;
    # solo explica cada cambio que ocurre sobre inventario_sucursal.
    op.create_table(
        "movimientos_inventario",
        sa.Column("id_movimiento", sa.Integer(), nullable=False),
        sa.Column("id_inventario", sa.Integer(), nullable=False),
        sa.Column("id_usuario", sa.Integer(), nullable=False),
        sa.Column("tipo_movimiento", sa.String(length=80), nullable=False),
        sa.Column("motivo", sa.String(length=255), nullable=True),
        sa.Column("cantidad", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("fecha_hora", sa.DateTime(), nullable=False),
        sa.Column("modulo_origen", sa.String(length=80), nullable=True),
        sa.Column("id_origen", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_inventario"], ["inventario_sucursal.id_inventario"]),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuarios.id_usuario"]),
        sa.PrimaryKeyConstraint("id_movimiento"),
    )


def downgrade():
    op.drop_table("movimientos_inventario")
