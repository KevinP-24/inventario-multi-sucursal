from app.extensions import db
from app.modules.inventario.tipo_movimiento_inventario.model import TipoMovimientoInventario


def consultar_todos_los_tipos_movimiento_inventario_en_bd():
    """Consulta en PostgreSQL todos los tipos de movimiento ordenados por nombre."""
    return TipoMovimientoInventario.query.order_by(TipoMovimientoInventario.nombre.asc()).all()


def consultar_tipo_movimiento_inventario_por_id_en_bd(id_tipo_movimiento):
    """Consulta en PostgreSQL un tipo de movimiento usando su id."""
    return TipoMovimientoInventario.query.get(id_tipo_movimiento)


def consultar_tipo_movimiento_inventario_por_nombre_en_bd(nombre):
    """Consulta si ya existe un tipo de movimiento con ese nombre."""
    return TipoMovimientoInventario.query.filter_by(nombre=nombre).first()


def guardar_tipo_movimiento_inventario_en_base_de_datos(tipo_movimiento):
    """Inserta o actualiza un tipo de movimiento en PostgreSQL."""
    db.session.add(tipo_movimiento)
    db.session.commit()
    return tipo_movimiento
