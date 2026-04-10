from app.extensions import db
from app.modules.auth.usuario.model import Usuario


def consultar_todos_los_usuarios_en_bd():
    """Consulta en PostgreSQL todos los usuarios ordenados por nombre."""
    return Usuario.query.order_by(Usuario.nombre.asc()).all()


def consultar_usuario_por_id_en_bd(id_usuario):
    """Consulta en PostgreSQL un usuario usando su id."""
    return Usuario.query.get(id_usuario)


def consultar_usuario_por_correo_en_bd(correo):
    """Consulta en PostgreSQL un usuario usando su correo.

    Esta consulta sirve para evitar correos repetidos y luego tambien servira
    para login.
    """
    return Usuario.query.filter_by(correo=correo).first()


def guardar_usuario_en_base_de_datos(usuario):
    """Inserta o actualiza un usuario en PostgreSQL."""
    db.session.add(usuario)
    db.session.commit()
    return usuario
