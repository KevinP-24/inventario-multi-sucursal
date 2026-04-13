"""crear proveedores y producto unidades

Revision ID: adf7d0cb03bb
Revises: 4cc8fd868038
Create Date: 2026-04-09 23:45:00.012412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adf7d0cb03bb'
down_revision = '4cc8fd868038'
branch_labels = None
depends_on = None


def upgrade():
    # Proveedores es un catalogo tranquilo que despues usaran las ordenes de compra.
    op.create_table('proveedores',
    sa.Column('id_proveedor', sa.Integer(), nullable=False),
    sa.Column('nit', sa.String(length=40), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.Column('correo', sa.String(length=120), nullable=True),
    sa.Column('telefono', sa.String(length=30), nullable=True),
    sa.Column('direccion', sa.String(length=180), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_proveedor'),
    sa.UniqueConstraint('nit')
    )
    # Producto-unidad explica como se mide o empaca un producto.
    # Ejemplo: mouse por unidad o caja de 20 unidades.
    op.create_table('producto_unidades',
    sa.Column('id_producto_unidad', sa.Integer(), nullable=False),
    sa.Column('id_producto', sa.Integer(), nullable=False),
    sa.Column('id_unidad', sa.Integer(), nullable=False),
    sa.Column('factor_conversion', sa.Numeric(precision=12, scale=4), nullable=False),
    sa.Column('es_base', sa.Boolean(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ),
    sa.ForeignKeyConstraint(['id_unidad'], ['unidades_medida.id_unidad'], ),
    sa.PrimaryKeyConstraint('id_producto_unidad'),
    sa.UniqueConstraint('id_producto', 'id_unidad', name='uq_producto_unidad')
    )


def downgrade():
    # Primero quitamos producto_unidades porque depende de productos y unidades_medida.
    op.drop_table('producto_unidades')
    op.drop_table('proveedores')
