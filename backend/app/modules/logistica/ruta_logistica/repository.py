from app.extensions import db
from app.modules.logistica.ruta_logistica.model import RutaLogistica


def consultar_todas_las_rutas_logistica_en_bd():
    """Consulta en PostgreSQL todas las rutas logisticas ordenadas por nombre."""
    return RutaLogistica.query.order_by(RutaLogistica.nombre_ruta.asc()).all()


def consultar_ruta_logistica_por_id_en_bd(id_ruta):
    """Consulta en PostgreSQL una ruta logistica usando su id."""
    return RutaLogistica.query.get(id_ruta)


def consultar_ruta_logistica_por_nombre_en_bd(nombre_ruta):
    """Consulta si ya existe una ruta logistica con ese nombre."""
    return RutaLogistica.query.filter_by(nombre_ruta=nombre_ruta).first()


def guardar_ruta_logistica_en_base_de_datos(ruta_logistica):
    """Inserta o actualiza una ruta logistica en PostgreSQL."""
    db.session.add(ruta_logistica)
    db.session.commit()
    return ruta_logistica
