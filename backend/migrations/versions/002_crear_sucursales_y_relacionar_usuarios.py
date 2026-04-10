"""crear sucursales y relacionar usuarios

Revision ID: a3b51e148bb3
Revises: 91ee57aa0b95
Create Date: 2026-04-09 23:18:00.114575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3b51e148bb3'
down_revision = '91ee57aa0b95'
branch_labels = None
depends_on = None


def upgrade():
    # Creamos sucursales antes de relacionarla con usuarios.
    op.create_table('sucursales',
    sa.Column('id_sucursal', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=120), nullable=False),
    sa.Column('direccion', sa.String(length=180), nullable=False),
    sa.Column('ciudad', sa.String(length=80), nullable=False),
    sa.Column('telefono', sa.String(length=30), nullable=True),
    sa.Column('estado', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id_sucursal'),
    sa.UniqueConstraint('nombre')
    )
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        # id_sucursal puede quedar vacio para el Admin general, que tiene alcance global.
        batch_op.create_foreign_key(
            'fk_usuarios_id_sucursal_sucursales',
            'sucursales',
            ['id_sucursal'],
            ['id_sucursal'],
        )


def downgrade():
    # Primero quitamos la relacion y despues la tabla de sucursales.
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_constraint('fk_usuarios_id_sucursal_sucursales', type_='foreignkey')

    op.drop_table('sucursales')
