from app.extensions import db
from app.modules.transferencias.recepcion_transferencia.model import RecepcionTransferencia


def consultar_recepciones_por_transferencia_en_bd(id_transferencia):
    """Consulta recepciones registradas para una transferencia."""
    return RecepcionTransferencia.query.filter_by(id_transferencia=id_transferencia).order_by(
        RecepcionTransferencia.id_recepcion.asc(),
    ).all()


def guardar_recepcion_transferencia_en_base_de_datos(recepcion):
    """Inserta o actualiza una recepcion de transferencia."""
    db.session.add(recepcion)
    db.session.commit()
    return recepcion
