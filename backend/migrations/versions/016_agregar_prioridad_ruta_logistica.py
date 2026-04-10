"""normalizar prioridad ruta logistica

Revision ID: 16c7d8e9f0a1
Revises: 15b6c7d8e9f0
Create Date: 2026-04-10 12:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16c7d8e9f0a1"
down_revision = "15b6c7d8e9f0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "prioridades_ruta_logistica",
        sa.Column("id_prioridad_ruta", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id_prioridad_ruta"),
        sa.UniqueConstraint("nombre"),
    )

    op.execute("""
        insert into prioridades_ruta_logistica (nombre, descripcion) values
        ('BAJA', 'Ruta de baja prioridad operativa.'),
        ('NORMAL', 'Ruta de prioridad operativa normal.'),
        ('ALTA', 'Ruta prioritaria para despachos frecuentes o sensibles.'),
        ('URGENTE', 'Ruta critica para despachos urgentes.')
    """)

    with op.batch_alter_table("rutas_logistica", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("id_prioridad_ruta", sa.Integer(), nullable=True)
        )

    op.execute("""
        update rutas_logistica
        set id_prioridad_ruta = (
            select id_prioridad_ruta
            from prioridades_ruta_logistica
            where nombre = 'NORMAL'
        )
    """)

    with op.batch_alter_table("rutas_logistica", schema=None) as batch_op:
        batch_op.alter_column("id_prioridad_ruta", nullable=False)
        batch_op.create_foreign_key(
            "fk_rutas_logistica_prioridad_ruta",
            "prioridades_ruta_logistica",
            ["id_prioridad_ruta"],
            ["id_prioridad_ruta"],
        )


def downgrade():
    with op.batch_alter_table("rutas_logistica", schema=None) as batch_op:
        batch_op.drop_constraint("fk_rutas_logistica_prioridad_ruta", type_="foreignkey")
        batch_op.drop_column("id_prioridad_ruta")

    op.drop_table("prioridades_ruta_logistica")
