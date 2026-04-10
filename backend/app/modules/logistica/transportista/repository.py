from app.extensions import db
from app.modules.logistica.transportista.model import Transportista


def consultar_todos_los_transportistas_en_bd():
    """Consulta en PostgreSQL todos los transportistas ordenados por nombre."""
    return Transportista.query.order_by(Transportista.nombre.asc()).all()


def consultar_transportista_por_id_en_bd(id_transportista):
    """Consulta en PostgreSQL un transportista usando su id."""
    return Transportista.query.get(id_transportista)


def consultar_transportista_por_identificacion_en_bd(identificacion):
    """Consulta si ya existe un transportista con esa identificacion."""
    return Transportista.query.filter_by(identificacion=identificacion).first()


def guardar_transportista_en_base_de_datos(transportista):
    """Inserta o actualiza un transportista en PostgreSQL."""
    db.session.add(transportista)
    db.session.commit()
    return transportista
