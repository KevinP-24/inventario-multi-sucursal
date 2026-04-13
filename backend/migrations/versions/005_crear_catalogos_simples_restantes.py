"""crear catalogos simples restantes

Revision ID: 45846a03dd5a
Revises: adf7d0cb03bb
Create Date: 2026-04-09 23:54:52.775423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45846a03dd5a'
down_revision = 'adf7d0cb03bb'
branch_labels = None
depends_on = None


def upgrade():
    # Catalogos comerciales para preparar ventas sin crear transacciones todavia.
    op.create_table('listas_precio',
    sa.Column('id_lista_precio', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=120), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('activa', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_lista_precio'),
    sa.UniqueConstraint('nombre')
    )
    # Parametros simples de configuracion general del sistema.
    op.create_table('parametros_sistema',
    sa.Column('id_parametro', sa.Integer(), nullable=False),
    sa.Column('clave', sa.String(length=120), nullable=False),
    sa.Column('valor', sa.String(length=255), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_parametro'),
    sa.UniqueConstraint('clave')
    )
    # Catalogos logisticos para preparar transferencias futuras.
    op.create_table('rutas_logistica',
    sa.Column('id_ruta', sa.Integer(), nullable=False),
    sa.Column('nombre_ruta', sa.String(length=120), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('costo_estimado', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('tiempo_estimado', sa.String(length=80), nullable=True),
    sa.Column('activa', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_ruta'),
    sa.UniqueConstraint('nombre_ruta')
    )
    op.create_table('transportistas',
    sa.Column('id_transportista', sa.Integer(), nullable=False),
    sa.Column('identificacion', sa.String(length=40), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.Column('telefono', sa.String(length=30), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_transportista'),
    sa.UniqueConstraint('identificacion')
    )
    # Precios por producto y lista. Esto prepara ventas, pero aun no registra ventas.
    op.create_table('precios_producto',
    sa.Column('id_precio_producto', sa.Integer(), nullable=False),
    sa.Column('id_producto', sa.Integer(), nullable=False),
    sa.Column('id_lista_precio', sa.Integer(), nullable=False),
    sa.Column('precio', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('fecha_vigencia', sa.Date(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_lista_precio'], ['listas_precio.id_lista_precio'], ),
    sa.ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ),
    sa.PrimaryKeyConstraint('id_precio_producto'),
    sa.UniqueConstraint('id_producto', 'id_lista_precio', name='uq_producto_lista_precio')
    )


def downgrade():
    # Primero precios porque depende de productos y listas_precio.
    op.drop_table('precios_producto')
    op.drop_table('transportistas')
    op.drop_table('rutas_logistica')
    op.drop_table('parametros_sistema')
    op.drop_table('listas_precio')
