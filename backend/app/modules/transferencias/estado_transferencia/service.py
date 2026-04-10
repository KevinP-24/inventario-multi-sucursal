from app.modules.transferencias.estado_transferencia.repository import (
    consultar_todos_los_estados_transferencia_en_bd,
)
from app.modules.transferencias.estado_transferencia.schema import (
    convertir_estado_transferencia_a_respuesta,
)


def listar_estados_transferencia_para_respuesta():
    """Consulta el catalogo de estados de transferencia para API."""
    estados = consultar_todos_los_estados_transferencia_en_bd()
    return [convertir_estado_transferencia_a_respuesta(estado) for estado in estados]
