from app.extensions import db
from app.modules.sucursales.sucursal.model import Sucursal


def consultar_todas_las_sucursales_en_bd():
    """Consulta en PostgreSQL todas las sucursales ordenadas por nombre."""
    return Sucursal.query.order_by(Sucursal.nombre.asc()).all()


def consultar_sucursal_por_id_en_bd(id_sucursal):
    """Consulta en PostgreSQL una sucursal usando su id."""
    return Sucursal.query.get(id_sucursal)


def consultar_sucursal_por_nombre_en_bd(nombre):
    """Consulta en PostgreSQL si ya existe una sucursal con ese nombre."""
    return Sucursal.query.filter_by(nombre=nombre).first()


def guardar_sucursal_en_base_de_datos(sucursal):
    """Inserta o actualiza una sucursal en PostgreSQL."""
    db.session.add(sucursal)
    db.session.commit()
    return sucursal
