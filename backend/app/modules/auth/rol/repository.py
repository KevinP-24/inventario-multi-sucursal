from app.extensions import db
from app.modules.auth.rol.model import Rol


def consultar_todos_los_roles_en_bd():
    """Consulta en PostgreSQL todos los roles ordenados por nombre."""
    return Rol.query.order_by(Rol.nombre.asc()).all()


def consultar_rol_por_id_en_bd(id_rol):
    """Consulta en PostgreSQL un rol usando su id."""
    return Rol.query.get(id_rol)


def consultar_rol_por_nombre_en_bd(nombre):
    """Consulta en PostgreSQL si ya existe un rol con ese nombre."""
    return Rol.query.filter_by(nombre=nombre).first()


def guardar_rol_en_base_de_datos(rol):
    """Inserta o actualiza un rol en PostgreSQL."""
    db.session.add(rol)
    db.session.commit()
    return rol
