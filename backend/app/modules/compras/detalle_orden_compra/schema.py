def convertir_detalle_orden_compra_a_respuesta(detalle):
    """Convierte un detalle SQLAlchemy a diccionario para responder por API."""
    return detalle.convertir_a_diccionario()
