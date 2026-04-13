from app.extensions import db
from app.modules.transferencias.transferencia.model import Transferencia


def consultar_todas_las_transferencias_en_bd():
    """Consulta todas las transferencias, de la mas reciente a la mas antigua."""
    return Transferencia.query.order_by(Transferencia.id_transferencia.desc()).all()


def consultar_transferencia_por_id_en_bd(id_transferencia):
    """Consulta una transferencia usando su id."""
    return Transferencia.query.get(id_transferencia)


def guardar_transferencia_en_base_de_datos(transferencia):
    """Inserta o actualiza una transferencia."""
    db.session.add(transferencia)
    db.session.commit()
    return transferencia
