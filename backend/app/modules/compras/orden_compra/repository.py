from app.extensions import db
from app.modules.compras.detalle_orden_compra.model import DetalleOrdenCompra
from app.modules.compras.orden_compra.model import OrdenCompra


def consultar_todas_las_ordenes_compra_en_bd():
    """Consulta en PostgreSQL todas las ordenes, de la mas reciente a la mas antigua."""
    return OrdenCompra.query.order_by(OrdenCompra.id_orden_compra.desc()).all()


def consultar_orden_compra_por_id_en_bd(id_orden_compra):
    """Consulta en PostgreSQL una orden de compra usando su id."""
    return OrdenCompra.query.get(id_orden_compra)


def filtrar_ordenes_compra_en_bd(filtros):
    """Consulta historico de compras por proveedor, producto y fechas."""
    consulta = OrdenCompra.query

    if filtros.get("id_producto"):
        consulta = consulta.join(
            DetalleOrdenCompra,
            OrdenCompra.id_orden_compra == DetalleOrdenCompra.id_orden_compra,
        ).filter(DetalleOrdenCompra.id_producto == filtros["id_producto"])

    if filtros.get("id_proveedor"):
        consulta = consulta.filter(OrdenCompra.id_proveedor == filtros["id_proveedor"])

    if filtros.get("id_sucursal"):
        consulta = consulta.filter(OrdenCompra.id_sucursal == filtros["id_sucursal"])

    if filtros.get("estado"):
        consulta = consulta.filter(OrdenCompra.estado == filtros["estado"])

    if filtros.get("fecha_desde"):
        consulta = consulta.filter(OrdenCompra.fecha >= filtros["fecha_desde"])

    if filtros.get("fecha_hasta"):
        consulta = consulta.filter(OrdenCompra.fecha <= filtros["fecha_hasta"])

    return consulta.order_by(OrdenCompra.fecha.desc(), OrdenCompra.id_orden_compra.desc()).all()


def guardar_orden_compra_en_base_de_datos(orden_compra):
    """Inserta o actualiza una orden de compra en PostgreSQL."""
    db.session.add(orden_compra)
    db.session.commit()
    return orden_compra
