"""normalizar tipos documento cliente

Revision ID: 14a5b6c7d8e9
Revises: 13f4a5b6c7d8
Create Date: 2026-04-10 03:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "14a5b6c7d8e9"
down_revision = "13f4a5b6c7d8"
branch_labels = None
depends_on = None


def upgrade():
    # Catalogo colombiano de documentos de identificacion para clientes.
    op.create_table(
        "tipos_documento",
        sa.Column("id_tipo_documento", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=20), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id_tipo_documento"),
        sa.UniqueConstraint("codigo"),
    )

    op.execute("""
        insert into tipos_documento (codigo, nombre, descripcion, activo) values
        ('CC', 'Cedula de ciudadania', 'Documento de identificacion para ciudadanos colombianos mayores de edad.', true),
        ('TI', 'Tarjeta de identidad', 'Documento de identificacion para menores de edad en Colombia.', true),
        ('CE', 'Cedula de extranjeria', 'Documento para extranjeros residentes en Colombia.', true),
        ('NIT', 'Numero de identificacion tributaria', 'Identificacion tributaria de empresas o personas ante la DIAN.', true),
        ('PAS', 'Pasaporte', 'Documento de viaje usado como identificacion.', true),
        ('PEP', 'Permiso especial de permanencia', 'Documento usado por poblacion migrante segun disposiciones colombianas.', true),
        ('PPT', 'Permiso por proteccion temporal', 'Documento de identificacion para poblacion migrante venezolana en Colombia.', true)
    """)

    with op.batch_alter_table("clientes", schema=None) as batch_op:
        batch_op.add_column(sa.Column("id_tipo_documento", sa.Integer(), nullable=True))

    op.execute("""
        update clientes cliente
        set id_tipo_documento = tipo.id_tipo_documento
        from tipos_documento tipo
        where tipo.codigo = upper(cliente.tipo_documento)
    """)

    op.execute("""
        update clientes
        set id_tipo_documento = (
            select id_tipo_documento from tipos_documento where codigo = 'CC'
        )
        where id_tipo_documento is null
    """)

    with op.batch_alter_table("clientes", schema=None) as batch_op:
        batch_op.alter_column("id_tipo_documento", nullable=False)
        batch_op.create_foreign_key(
            "fk_clientes_tipo_documento",
            "tipos_documento",
            ["id_tipo_documento"],
            ["id_tipo_documento"],
        )
        batch_op.drop_column("tipo_documento")


def downgrade():
    with op.batch_alter_table("clientes", schema=None) as batch_op:
        batch_op.add_column(sa.Column("tipo_documento", sa.String(length=30), nullable=True))

    op.execute("""
        update clientes cliente
        set tipo_documento = tipo.codigo
        from tipos_documento tipo
        where tipo.id_tipo_documento = cliente.id_tipo_documento
    """)

    with op.batch_alter_table("clientes", schema=None) as batch_op:
        batch_op.alter_column("tipo_documento", nullable=False)
        batch_op.drop_constraint("fk_clientes_tipo_documento", type_="foreignkey")
        batch_op.drop_column("id_tipo_documento")

    op.drop_table("tipos_documento")
