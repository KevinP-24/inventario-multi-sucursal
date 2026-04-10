"""normalizar documento proveedor

Revision ID: 15b6c7d8e9f0
Revises: 14a5b6c7d8e9
Create Date: 2026-04-10 03:25:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "15b6c7d8e9f0"
down_revision = "14a5b6c7d8e9"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proveedores", schema=None) as batch_op:
        batch_op.add_column(sa.Column("id_tipo_documento", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("numero_documento", sa.String(length=40), nullable=True))

    op.execute("""
        update proveedores
        set numero_documento = nit,
            id_tipo_documento = (
                select id_tipo_documento from tipos_documento where codigo = 'NIT'
            )
    """)

    with op.batch_alter_table("proveedores", schema=None) as batch_op:
        batch_op.alter_column("id_tipo_documento", nullable=False)
        batch_op.alter_column("numero_documento", nullable=False)
        batch_op.create_foreign_key(
            "fk_proveedores_tipo_documento",
            "tipos_documento",
            ["id_tipo_documento"],
            ["id_tipo_documento"],
        )
        batch_op.create_unique_constraint("uq_proveedores_numero_documento", ["numero_documento"])
        batch_op.drop_column("nit")


def downgrade():
    with op.batch_alter_table("proveedores", schema=None) as batch_op:
        batch_op.add_column(sa.Column("nit", sa.String(length=40), nullable=True))

    op.execute("""
        update proveedores
        set nit = numero_documento
    """)

    with op.batch_alter_table("proveedores", schema=None) as batch_op:
        batch_op.alter_column("nit", nullable=False)
        batch_op.create_unique_constraint("proveedores_nit_key", ["nit"])
        batch_op.drop_constraint("uq_proveedores_numero_documento", type_="unique")
        batch_op.drop_constraint("fk_proveedores_tipo_documento", type_="foreignkey")
        batch_op.drop_column("numero_documento")
        batch_op.drop_column("id_tipo_documento")
