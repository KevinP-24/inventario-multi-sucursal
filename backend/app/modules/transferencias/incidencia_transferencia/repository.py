from app.modules.transferencias.incidencia_transferencia.model import IncidenciaTransferencia


def consultar_incidencias_por_recepcion_en_bd(id_recepcion):
    """Consulta faltantes o diferencias de una recepcion."""
    return IncidenciaTransferencia.query.filter_by(id_recepcion=id_recepcion).order_by(
        IncidenciaTransferencia.id_incidencia.asc(),
    ).all()
