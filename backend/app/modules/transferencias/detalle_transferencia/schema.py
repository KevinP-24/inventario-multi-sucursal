def convertir_detalle_transferencia_a_respuesta(detalle):
    """Convierte un detalle SQLAlchemy a diccionario."""
    return detalle.convertir_a_diccionario()
