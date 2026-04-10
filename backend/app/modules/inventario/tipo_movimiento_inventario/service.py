from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_todos_los_tipos_movimiento_inventario_en_bd,
)
from app.modules.inventario.tipo_movimiento_inventario.schema import (
    convertir_tipo_movimiento_inventario_a_respuesta,
)


def listar_tipos_movimiento_inventario_para_respuesta():
    """Consulta el catalogo de tipos de movimiento y lo deja listo para API."""
    tipos = consultar_todos_los_tipos_movimiento_inventario_en_bd()
    return [convertir_tipo_movimiento_inventario_a_respuesta(tipo) for tipo in tipos]
