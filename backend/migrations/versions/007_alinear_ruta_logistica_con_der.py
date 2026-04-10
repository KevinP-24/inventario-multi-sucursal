"""alinear ruta logistica con der

Revision ID: 7f2b83d6c1a4
Revises: 2cd62284359b
Create Date: 2026-04-10 00:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7f2b83d6c1a4"
down_revision = "2cd62284359b"
branch_labels = None
depends_on = None


def upgrade():
    # Dejamos rutas_logistica igual al DER:
    # id_ruta, nombre_ruta, costo_estimado y tiempo_estimado.
    # Origen y destino viven en transferencia, no en la ruta.
    with op.batch_alter_table("rutas_logistica", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_rutas_logistica_sucursal_destino",
            type_="foreignkey",
        )
        batch_op.drop_constraint(
            "fk_rutas_logistica_sucursal_origen",
            type_="foreignkey",
        )
        batch_op.drop_column("id_sucursal_destino")
        batch_op.drop_column("id_sucursal_origen")
        batch_op.drop_column("activa")
        batch_op.drop_column("descripcion")


def downgrade():
    # Volvemos al estado anterior solo si algun dia se necesita reversar.
    with op.batch_alter_table("rutas_logistica", schema=None) as batch_op:
        batch_op.add_column(sa.Column("descripcion", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("activa", sa.Boolean(), nullable=False, server_default=sa.true()))
        batch_op.add_column(sa.Column("id_sucursal_origen", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("id_sucursal_destino", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_rutas_logistica_sucursal_origen",
            "sucursales",
            ["id_sucursal_origen"],
            ["id_sucursal"],
        )
        batch_op.create_foreign_key(
            "fk_rutas_logistica_sucursal_destino",
            "sucursales",
            ["id_sucursal_destino"],
            ["id_sucursal"],
        )

    op.alter_column("rutas_logistica", "activa", server_default=None)
