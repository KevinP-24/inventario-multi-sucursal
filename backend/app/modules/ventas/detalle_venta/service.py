from app.modules.ventas.detalle_venta.repository import consultar_detalles_por_venta_en_bd
from app.modules.ventas.detalle_venta.schema import convertir_detalle_venta_a_respuesta


def listar_detalles_por_venta_para_respuesta(id_venta):
    """Consulta los detalles de una venta y los deja listos para API."""
    detalles = consultar_detalles_por_venta_en_bd(id_venta)
    return [convertir_detalle_venta_a_respuesta(detalle) for detalle in detalles]
