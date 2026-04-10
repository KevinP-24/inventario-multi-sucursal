from app.modules.ventas.detalle_venta.model import DetalleVenta


def consultar_detalles_por_venta_en_bd(id_venta):
    """Consulta los productos vendidos dentro de una venta."""
    return DetalleVenta.query.filter_by(id_venta=id_venta).order_by(
        DetalleVenta.id_detalle_venta.asc(),
    ).all()
