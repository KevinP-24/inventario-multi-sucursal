from app.modules.ventas.tipo_documento.repository import (
    consultar_todos_los_tipos_documento_en_bd,
)
from app.modules.ventas.tipo_documento.schema import convertir_tipo_documento_a_respuesta


def listar_tipos_documento_para_respuesta():
    """Consulta el catalogo de tipos de documento para API."""
    tipos = consultar_todos_los_tipos_documento_en_bd()
    return [convertir_tipo_documento_a_respuesta(tipo) for tipo in tipos]
