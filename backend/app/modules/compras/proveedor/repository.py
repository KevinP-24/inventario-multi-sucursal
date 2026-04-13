from app.extensions import db
from app.modules.compras.proveedor.model import Proveedor


def consultar_todos_los_proveedores_en_bd():
    """Consulta en PostgreSQL todos los proveedores ordenados por nombre."""
    return Proveedor.query.order_by(Proveedor.nombre.asc()).all()


def consultar_proveedor_por_id_en_bd(id_proveedor):
    """Consulta en PostgreSQL un proveedor usando su id."""
    return Proveedor.query.get(id_proveedor)


def consultar_proveedor_por_documento_en_bd(numero_documento):
    """Consulta en PostgreSQL si ya existe un proveedor con ese documento."""
    return Proveedor.query.filter_by(numero_documento=numero_documento).first()


def guardar_proveedor_en_base_de_datos(proveedor):
    """Inserta o actualiza un proveedor en PostgreSQL."""
    db.session.add(proveedor)
    db.session.commit()
    return proveedor
