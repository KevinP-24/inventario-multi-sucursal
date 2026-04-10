PRIORIDADES_RUTA_LOGISTICA_BASE = [
    {
        "nombre": "BAJA",
        "descripcion": "Ruta de baja prioridad operativa.",
    },
    {
        "nombre": "NORMAL",
        "descripcion": "Ruta de prioridad operativa normal.",
    },
    {
        "nombre": "ALTA",
        "descripcion": "Ruta prioritaria para despachos frecuentes o sensibles.",
    },
    {
        "nombre": "URGENTE",
        "descripcion": "Ruta critica para despachos urgentes.",
    },
]


def convertir_prioridad_ruta_logistica_a_respuesta(prioridad):
    """Convierte una prioridad SQLAlchemy a diccionario."""
    return prioridad.convertir_a_diccionario()
