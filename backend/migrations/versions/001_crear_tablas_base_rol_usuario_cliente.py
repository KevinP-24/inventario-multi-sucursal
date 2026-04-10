"""crear tablas base rol usuario cliente

Revision ID: 91ee57aa0b95
Revises: 
Create Date: 2026-04-09 22:39:20.582439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91ee57aa0b95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Creamos primero clientes y roles porque no dependen de otras tablas.
    op.create_table('clientes',
    sa.Column('id_cliente', sa.Integer(), nullable=False),
    sa.Column('tipo_documento', sa.String(length=30), nullable=False),
    sa.Column('numero_documento', sa.String(length=40), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.Column('correo', sa.String(length=120), nullable=True),
    sa.Column('telefono', sa.String(length=30), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id_cliente'),
    sa.UniqueConstraint('numero_documento')
    )
    op.create_table('roles',
    sa.Column('id_rol', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id_rol'),
    sa.UniqueConstraint('nombre')
    )
    # Usuarios depende de roles porque cada usuario debe tener un perfil.
    op.create_table('usuarios',
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_rol', sa.Integer(), nullable=False),
    sa.Column('id_sucursal', sa.Integer(), nullable=True),
    sa.Column('nombre', sa.String(length=120), nullable=False),
    sa.Column('correo', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], ),
    sa.PrimaryKeyConstraint('id_usuario'),
    sa.UniqueConstraint('correo')
    )


def downgrade():
    # Para reversar, se borra primero usuarios porque depende de roles.
    op.drop_table('usuarios')
    op.drop_table('roles')
    op.drop_table('clientes')
