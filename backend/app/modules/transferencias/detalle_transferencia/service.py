from app.modules.transferencias.detalle_transferencia.repository import (
    consultar_detalles_por_transferencia_en_bd,
)
from app.modules.transferencias.detalle_transferencia.schema import (
    convertir_detalle_transferencia_a_respuesta,
)


def listar_detalles_por_transferencia_para_respuesta(id_transferencia):
    """Consulta los detalles de una transferencia para API."""
    detalles = consultar_detalles_por_transferencia_en_bd(id_transferencia)
    return [convertir_detalle_transferencia_a_respuesta(detalle) for detalle in detalles]
