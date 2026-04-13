from app.extensions import db
from app.modules.transferencias.estado_transferencia.model import EstadoTransferencia


def consultar_todos_los_estados_transferencia_en_bd():
    """Consulta todos los estados de transferencia ordenados por nombre."""
    return EstadoTransferencia.query.order_by(EstadoTransferencia.nombre.asc()).all()


def consultar_estado_transferencia_por_nombre_en_bd(nombre):
    """Consulta un estado de transferencia usando su nombre logico."""
    return EstadoTransferencia.query.filter_by(nombre=nombre).first()


def guardar_estado_transferencia_en_base_de_datos(estado):
    """Inserta o actualiza un estado de transferencia."""
    db.session.add(estado)
    db.session.commit()
    return estado
