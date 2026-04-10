"""agregar origen y destino a rutas logisticas

Revision ID: 2cd62284359b
Revises: 45846a03dd5a
Create Date: 2026-04-10 00:01:25.547881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd62284359b'
down_revision = '45846a03dd5a'
branch_labels = None
depends_on = None


def upgrade():
    # Agregamos origen y destino como nullable primero para poder actualizar
    # las rutas demo existentes sin romper la migracion.
    with op.batch_alter_table('rutas_logistica', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_sucursal_origen', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('id_sucursal_destino', sa.Integer(), nullable=True))

    # Completamos las rutas demo ya creadas por el seeder anterior.
    op.execute("""
        update rutas_logistica
        set id_sucursal_origen = (
            select id_sucursal from sucursales
            where nombre = 'Sucursal Centro Tecnologico'
        ),
        id_sucursal_destino = (
            select id_sucursal from sucursales
            where nombre = 'Sucursal Norte Empresarial'
        )
        where nombre_ruta = 'Centro Tecnologico - Norte Empresarial'
    """)

    op.execute("""
        update rutas_logistica
        set id_sucursal_origen = (
            select id_sucursal from sucursales
            where nombre = 'Sucursal Centro Tecnologico'
        ),
        id_sucursal_destino = (
            select id_sucursal from sucursales
            where nombre = 'Sucursal Outlet Sur'
        )
        where nombre_ruta = 'Centro Tecnologico - Outlet Sur'
    """)

    with op.batch_alter_table('rutas_logistica', schema=None) as batch_op:
        batch_op.alter_column('id_sucursal_origen', nullable=False)
        batch_op.alter_column('id_sucursal_destino', nullable=False)
        batch_op.create_foreign_key(
            'fk_rutas_logistica_sucursal_origen',
            'sucursales',
            ['id_sucursal_origen'],
            ['id_sucursal'],
        )
        batch_op.create_foreign_key(
            'fk_rutas_logistica_sucursal_destino',
            'sucursales',
            ['id_sucursal_destino'],
            ['id_sucursal'],
        )


def downgrade():
    # Quitamos primero las relaciones antes de quitar las columnas.
    with op.batch_alter_table('rutas_logistica', schema=None) as batch_op:
        batch_op.drop_constraint('fk_rutas_logistica_sucursal_destino', type_='foreignkey')
        batch_op.drop_constraint('fk_rutas_logistica_sucursal_origen', type_='foreignkey')
        batch_op.drop_column('id_sucursal_destino')
        batch_op.drop_column('id_sucursal_origen')
