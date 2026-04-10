def convertir_detalle_venta_a_respuesta(detalle_venta):
    """Convierte un detalle SQLAlchemy a diccionario para responder por API."""
    return detalle_venta.convertir_a_diccionario()
