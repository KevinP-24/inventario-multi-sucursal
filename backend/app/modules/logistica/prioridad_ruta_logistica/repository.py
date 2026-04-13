from app.extensions import db
from app.modules.logistica.prioridad_ruta_logistica.model import PrioridadRutaLogistica


def consultar_todas_las_prioridades_ruta_logistica_en_bd():
    """Consulta todas las prioridades logisticas ordenadas por criticidad."""
    prioridad_orden = db.case(
        (PrioridadRutaLogistica.nombre == "URGENTE", 1),
        (PrioridadRutaLogistica.nombre == "ALTA", 2),
        (PrioridadRutaLogistica.nombre == "NORMAL", 3),
        (PrioridadRutaLogistica.nombre == "BAJA", 4),
        else_=5,
    )
    return PrioridadRutaLogistica.query.order_by(prioridad_orden).all()


def consultar_prioridad_ruta_logistica_por_id_en_bd(id_prioridad_ruta):
    """Consulta una prioridad de ruta por id."""
    return PrioridadRutaLogistica.query.get(id_prioridad_ruta)


def consultar_prioridad_ruta_logistica_por_nombre_en_bd(nombre):
    """Consulta una prioridad de ruta usando su nombre logico."""
    return PrioridadRutaLogistica.query.filter_by(nombre=nombre).first()


def guardar_prioridad_ruta_logistica_en_base_de_datos(prioridad):
    """Inserta o actualiza una prioridad de ruta logistica."""
    db.session.add(prioridad)
    db.session.commit()
    return prioridad
