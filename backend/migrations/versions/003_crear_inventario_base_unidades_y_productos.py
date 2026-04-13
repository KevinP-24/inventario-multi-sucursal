"""crear inventario base unidades y productos

Revision ID: 4cc8fd868038
Revises: a3b51e148bb3
Create Date: 2026-04-09 23:30:18.389341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cc8fd868038'
down_revision = 'a3b51e148bb3'
branch_labels = None
depends_on = None


def upgrade():
    # Creamos productos como maestro basico de inventario.
    op.create_table('productos',
    sa.Column('id_producto', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=50), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('stock_minimo', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_producto'),
    sa.UniqueConstraint('codigo')
    )
    # Creamos unidades de medida para poder manejar productos por unidad, caja, kg, etc.
    op.create_table('unidades_medida',
    sa.Column('id_unidad', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('simbolo', sa.String(length=20), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_unidad'),
    sa.UniqueConstraint('nombre'),
    sa.UniqueConstraint('simbolo')
    )


def downgrade():
    # Reversamos en orden simple porque estas tablas aun no tienen dependencias.
    op.drop_table('unidades_medida')
    op.drop_table('productos')
