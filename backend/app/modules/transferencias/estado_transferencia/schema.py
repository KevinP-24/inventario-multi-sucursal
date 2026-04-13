ESTADOS_TRANSFERENCIA_BASE = [
    {
        "nombre": "SOLICITADA",
        "descripcion": "Transferencia registrada por la sucursal destino o un administrador.",
    },
    {
        "nombre": "APROBADA",
        "descripcion": "La sucursal origen reviso disponibilidad y aprobo cantidades.",
    },
    {
        "nombre": "ENVIADA",
        "descripcion": "La mercancia fue despachada desde la sucursal origen.",
    },
    {
        "nombre": "RECIBIDA",
        "descripcion": "La sucursal destino recibio toda la mercancia aprobada.",
    },
    {
        "nombre": "RECIBIDA_PARCIAL",
        "descripcion": "La sucursal destino recibio parcialmente y registro diferencias.",
    },
    {
        "nombre": "RECHAZADA",
        "descripcion": "La solicitud fue rechazada por la sucursal origen.",
    },
]


def convertir_estado_transferencia_a_respuesta(estado):
    """Convierte un estado SQLAlchemy a diccionario."""
    return estado.convertir_a_diccionario()
