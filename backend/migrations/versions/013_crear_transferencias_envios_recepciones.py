"""crear transferencias envios recepciones

Revision ID: 13f4a5b6c7d8
Revises: 12e3f4a5b6c7
Create Date: 2026-04-10 02:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "13f4a5b6c7d8"
down_revision = "12e3f4a5b6c7"
branch_labels = None
depends_on = None


def upgrade():
    # Catalogo normalizado para no guardar el ciclo de transferencia como texto suelto.
    op.create_table(
        "estados_transferencia",
        sa.Column("id_estado_transferencia", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id_estado_transferencia"),
        sa.UniqueConstraint("nombre"),
    )

    op.execute("""
        insert into estados_transferencia (nombre, descripcion) values
        ('SOLICITADA', 'Transferencia registrada por la sucursal destino o un administrador.'),
        ('APROBADA', 'La sucursal origen reviso disponibilidad y aprobo cantidades.'),
        ('ENVIADA', 'La mercancia fue despachada desde la sucursal origen.'),
        ('RECIBIDA', 'La sucursal destino recibio toda la mercancia aprobada.'),
        ('RECIBIDA_PARCIAL', 'La sucursal destino recibio parcialmente y registro diferencias.'),
        ('RECHAZADA', 'La solicitud fue rechazada por la sucursal origen.')
    """)

    op.create_table(
        "transferencia",
        sa.Column("id_transferencia", sa.Integer(), nullable=False),
        sa.Column("id_sucursal_origen", sa.Integer(), nullable=False),
        sa.Column("id_sucursal_destino", sa.Integer(), nullable=False),
        sa.Column("id_usuario_solicita", sa.Integer(), nullable=False),
        sa.Column("id_estado_transferencia", sa.Integer(), nullable=False),
        sa.Column("fecha_solicitud", sa.DateTime(), nullable=False),
        sa.Column("prioridad", sa.String(length=40), nullable=False),
        sa.Column("observacion", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["id_sucursal_origen"], ["sucursales.id_sucursal"]),
        sa.ForeignKeyConstraint(["id_sucursal_destino"], ["sucursales.id_sucursal"]),
        sa.ForeignKeyConstraint(["id_usuario_solicita"], ["usuarios.id_usuario"]),
        sa.ForeignKeyConstraint(
            ["id_estado_transferencia"],
            ["estados_transferencia.id_estado_transferencia"],
        ),
        sa.PrimaryKeyConstraint("id_transferencia"),
    )

    op.create_table(
        "detalle_transferencia",
        sa.Column("id_detalle_transferencia", sa.Integer(), nullable=False),
        sa.Column("id_transferencia", sa.Integer(), nullable=False),
        sa.Column("id_producto", sa.Integer(), nullable=False),
        sa.Column("id_producto_unidad", sa.Integer(), nullable=False),
        sa.Column("cantidad_solicitada", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("cantidad_aprobada", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("cantidad_recibida", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["id_transferencia"], ["transferencia.id_transferencia"]),
        sa.ForeignKeyConstraint(["id_producto"], ["productos.id_producto"]),
        sa.ForeignKeyConstraint(["id_producto_unidad"], ["producto_unidades.id_producto_unidad"]),
        sa.PrimaryKeyConstraint("id_detalle_transferencia"),
    )

    op.create_table(
        "envio_transferencia",
        sa.Column("id_envio", sa.Integer(), nullable=False),
        sa.Column("id_transferencia", sa.Integer(), nullable=False),
        sa.Column("id_ruta", sa.Integer(), nullable=False),
        sa.Column("id_transportista", sa.Integer(), nullable=False),
        sa.Column("fecha_envio", sa.DateTime(), nullable=False),
        sa.Column("fecha_estimada_llegada", sa.DateTime(), nullable=True),
        sa.Column("fecha_real_llegada", sa.DateTime(), nullable=True),
        sa.Column("estado_envio", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["id_transferencia"], ["transferencia.id_transferencia"]),
        sa.ForeignKeyConstraint(["id_ruta"], ["rutas_logistica.id_ruta"]),
        sa.ForeignKeyConstraint(["id_transportista"], ["transportistas.id_transportista"]),
        sa.PrimaryKeyConstraint("id_envio"),
        sa.UniqueConstraint("id_transferencia"),
    )

    op.create_table(
        "recepcion_transferencia",
        sa.Column("id_recepcion", sa.Integer(), nullable=False),
        sa.Column("id_transferencia", sa.Integer(), nullable=False),
        sa.Column("id_usuario_recibe", sa.Integer(), nullable=False),
        sa.Column("fecha_recepcion", sa.DateTime(), nullable=False),
        sa.Column("tipo_recepcion", sa.String(length=40), nullable=False),
        sa.Column("observacion", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["id_transferencia"], ["transferencia.id_transferencia"]),
        sa.ForeignKeyConstraint(["id_usuario_recibe"], ["usuarios.id_usuario"]),
        sa.PrimaryKeyConstraint("id_recepcion"),
    )

    op.create_table(
        "incidencia_transferencia",
        sa.Column("id_incidencia", sa.Integer(), nullable=False),
        sa.Column("id_recepcion", sa.Integer(), nullable=False),
        sa.Column("id_detalle_transferencia", sa.Integer(), nullable=False),
        sa.Column("cantidad_faltante", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("tratamiento", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["id_recepcion"], ["recepcion_transferencia.id_recepcion"]),
        sa.ForeignKeyConstraint(
            ["id_detalle_transferencia"],
            ["detalle_transferencia.id_detalle_transferencia"],
        ),
        sa.PrimaryKeyConstraint("id_incidencia"),
    )


def downgrade():
    op.drop_table("incidencia_transferencia")
    op.drop_table("recepcion_transferencia")
    op.drop_table("envio_transferencia")
    op.drop_table("detalle_transferencia")
    op.drop_table("transferencia")
    op.drop_table("estados_transferencia")
