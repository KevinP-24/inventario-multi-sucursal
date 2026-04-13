from app.modules.transferencias.detalle_transferencia.model import DetalleTransferencia


def consultar_detalles_por_transferencia_en_bd(id_transferencia):
    """Consulta los productos incluidos en una transferencia."""
    return DetalleTransferencia.query.filter_by(id_transferencia=id_transferencia).order_by(
        DetalleTransferencia.id_detalle_transferencia.asc(),
    ).all()
