from app.extensions import db
from app.modules.admin.parametro_sistema.model import ParametroSistema


def consultar_todos_los_parametros_sistema_en_bd():
    """Consulta en PostgreSQL todos los parametros ordenados por clave."""
    return ParametroSistema.query.order_by(ParametroSistema.clave.asc()).all()


def consultar_parametro_sistema_por_id_en_bd(id_parametro):
    """Consulta en PostgreSQL un parametro usando su id."""
    return ParametroSistema.query.get(id_parametro)


def consultar_parametro_sistema_por_clave_en_bd(clave):
    """Consulta en PostgreSQL si ya existe un parametro con esa clave."""
    return ParametroSistema.query.filter_by(clave=clave).first()


def guardar_parametro_sistema_en_base_de_datos(parametro):
    """Inserta o actualiza un parametro del sistema en PostgreSQL."""
    db.session.add(parametro)
    db.session.commit()
    return parametro
