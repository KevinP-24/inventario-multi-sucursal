from app.extensions import db
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.tipo_movimiento_inventario.model import TipoMovimientoInventario


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


def filtrar_movimientos_inventario_en_bd(filtros):
    """Consulta movimientos aplicando filtros utiles para auditoria."""
    consulta = MovimientoInventario.query.join(
        InventarioSucursal,
        MovimientoInventario.id_inventario == InventarioSucursal.id_inventario,
    )

    if filtros.get("id_inventario"):
        consulta = consulta.filter(MovimientoInventario.id_inventario == filtros["id_inventario"])

    if filtros.get("id_sucursal"):
        consulta = consulta.filter(InventarioSucursal.id_sucursal == filtros["id_sucursal"])

    if filtros.get("id_producto"):
        consulta = consulta.filter(InventarioSucursal.id_producto == filtros["id_producto"])

    if filtros.get("id_usuario"):
        consulta = consulta.filter(MovimientoInventario.id_usuario == filtros["id_usuario"])

    if filtros.get("id_tipo_movimiento"):
        consulta = consulta.filter(
            MovimientoInventario.id_tipo_movimiento == filtros["id_tipo_movimiento"]
        )

    if filtros.get("tipo_movimiento"):
        consulta = consulta.join(
            TipoMovimientoInventario,
            MovimientoInventario.id_tipo_movimiento
            == TipoMovimientoInventario.id_tipo_movimiento,
        ).filter(TipoMovimientoInventario.nombre == filtros["tipo_movimiento"])

    if filtros.get("modulo_origen"):
        consulta = consulta.filter(MovimientoInventario.modulo_origen == filtros["modulo_origen"])

    if filtros.get("id_origen"):
        consulta = consulta.filter(MovimientoInventario.id_origen == filtros["id_origen"])

    if filtros.get("fecha_desde"):
        consulta = consulta.filter(MovimientoInventario.fecha_hora >= filtros["fecha_desde"])

    if filtros.get("fecha_hasta"):
        consulta = consulta.filter(MovimientoInventario.fecha_hora <= filtros["fecha_hasta"])

    return consulta.order_by(MovimientoInventario.fecha_hora.desc()).all()


def guardar_movimiento_inventario_en_base_de_datos(movimiento):
    """Inserta un movimiento de inventario en PostgreSQL."""
    db.session.add(movimiento)
    db.session.commit()
    return movimiento
