from app.extensions import db
from app.modules.ventas.tipo_documento.model import TipoDocumento


def consultar_todos_los_tipos_documento_en_bd():
    """Consulta todos los tipos de documento activos e inactivos."""
    return TipoDocumento.query.order_by(TipoDocumento.codigo.asc()).all()


def consultar_tipo_documento_por_id_en_bd(id_tipo_documento):
    """Consulta un tipo de documento por id."""
    return TipoDocumento.query.get(id_tipo_documento)


def consultar_tipo_documento_por_codigo_en_bd(codigo):
    """Consulta un tipo de documento por codigo, por ejemplo CC o NIT."""
    return TipoDocumento.query.filter_by(codigo=codigo).first()


def guardar_tipo_documento_en_base_de_datos(tipo_documento):
    """Inserta o actualiza un tipo de documento."""
    db.session.add(tipo_documento)
    db.session.commit()
    return tipo_documento
