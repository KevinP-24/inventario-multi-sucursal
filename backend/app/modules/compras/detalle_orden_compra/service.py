from app.modules.compras.detalle_orden_compra.repository import (
    consultar_detalles_por_orden_compra_en_bd,
)
from app.modules.compras.detalle_orden_compra.schema import (
    convertir_detalle_orden_compra_a_respuesta,
)


def listar_detalles_por_orden_compra_para_respuesta(id_orden_compra):
    """Consulta los productos asociados a una orden de compra."""
    detalles = consultar_detalles_por_orden_compra_en_bd(id_orden_compra)
    return [convertir_detalle_orden_compra_a_respuesta(detalle) for detalle in detalles]
