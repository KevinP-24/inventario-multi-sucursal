from app.extensions import db
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario


def consultar_todos_los_movimientos_inventario_en_bd():
    """Consulta en PostgreSQL el historial completo, del mas reciente al mas antiguo."""
    return MovimientoInventario.query.order_by(MovimientoInventario.fecha_hora.desc()).all()


def consultar_movimiento_inventario_por_id_en_bd(id_movimiento):
    """Consulta en PostgreSQL un movimiento usando su id."""
    return MovimientoInventario.query.get(id_movimiento)


def consultar_movimientos_por_inventario_en_bd(id_inventario):
    """Consulta los movimientos de un producto en una sucursal especifica."""
    return (
        MovimientoInventario.query
        .filter_by(id_inventario=id_inventario)
        .order_by(MovimientoInventario.fecha_hora.desc())
        .all()
    )


def guardar_movimiento_inventario_en_base_de_datos(movimiento):
    """Inserta un movimiento de inventario en PostgreSQL."""
    db.session.add(movimiento)
    db.session.commit()
    return movimiento
