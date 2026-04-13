"""normalizar tipos movimiento inventario

Revision ID: 10c1d2e3f4a5
Revises: 9b7c6d5e4f30
Create Date: 2026-04-10 01:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "10c1d2e3f4a5"
down_revision = "9b7c6d5e4f30"
branch_labels = None
depends_on = None


def upgrade():
    # Catalogo atomico para no guardar el tipo como texto suelto en cada movimiento.
    op.create_table(
        "tipos_movimiento_inventario",
        sa.Column("id_tipo_movimiento", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id_tipo_movimiento"),
        sa.UniqueConstraint("nombre"),
    )

    op.execute("""
        insert into tipos_movimiento_inventario (nombre, descripcion) values
        ('ENTRADA', 'Aumenta inventario, por ejemplo al recibir una compra.'),
        ('SALIDA', 'Disminuye inventario, por ejemplo al confirmar una venta.'),
        ('AJUSTE', 'Corrige inventario por conteo fisico o ajuste manual.'),
        ('TRANSFERENCIA_ENTRADA', 'Entrada generada por recibir producto desde otra sucursal.'),
        ('TRANSFERENCIA_SALIDA', 'Salida generada por enviar producto hacia otra sucursal.')
    """)

    with op.batch_alter_table("movimientos_inventario", schema=None) as batch_op:
        batch_op.add_column(sa.Column("id_tipo_movimiento", sa.Integer(), nullable=True))

    op.execute("""
        update movimientos_inventario movimiento
        set id_tipo_movimiento = tipo.id_tipo_movimiento
        from tipos_movimiento_inventario tipo
        where tipo.nombre = movimiento.tipo_movimiento
    """)

    with op.batch_alter_table("movimientos_inventario", schema=None) as batch_op:
        batch_op.alter_column("id_tipo_movimiento", nullable=False)
        batch_op.create_foreign_key(
            "fk_movimientos_inventario_tipo_movimiento",
            "tipos_movimiento_inventario",
            ["id_tipo_movimiento"],
            ["id_tipo_movimiento"],
        )
        batch_op.drop_column("tipo_movimiento")


def downgrade():
    with op.batch_alter_table("movimientos_inventario", schema=None) as batch_op:
        batch_op.add_column(sa.Column("tipo_movimiento", sa.String(length=80), nullable=True))

    op.execute("""
        update movimientos_inventario movimiento
        set tipo_movimiento = tipo.nombre
        from tipos_movimiento_inventario tipo
        where tipo.id_tipo_movimiento = movimiento.id_tipo_movimiento
    """)

    with op.batch_alter_table("movimientos_inventario", schema=None) as batch_op:
        batch_op.alter_column("tipo_movimiento", nullable=False)
        batch_op.drop_constraint("fk_movimientos_inventario_tipo_movimiento", type_="foreignkey")
        batch_op.drop_column("id_tipo_movimiento")

    op.drop_table("tipos_movimiento_inventario")
