from app.extensions import db
from app.modules.inventario.unidad_medida.model import UnidadMedida


def consultar_todas_las_unidades_medida_en_bd():
    """Consulta en PostgreSQL todas las unidades de medida ordenadas por nombre."""
    return UnidadMedida.query.order_by(UnidadMedida.nombre.asc()).all()


def consultar_unidad_medida_por_id_en_bd(id_unidad):
    """Consulta en PostgreSQL una unidad de medida usando su id."""
    return UnidadMedida.query.get(id_unidad)


def consultar_unidad_medida_por_nombre_en_bd(nombre):
    """Consulta en PostgreSQL si ya existe una unidad con ese nombre."""
    return UnidadMedida.query.filter_by(nombre=nombre).first()


def consultar_unidad_medida_por_simbolo_en_bd(simbolo):
    """Consulta en PostgreSQL si ya existe una unidad con ese simbolo."""
    return UnidadMedida.query.filter_by(simbolo=simbolo).first()


def guardar_unidad_medida_en_base_de_datos(unidad_medida):
    """Inserta o actualiza una unidad de medida en PostgreSQL."""
    db.session.add(unidad_medida)
    db.session.commit()
    return unidad_medida
