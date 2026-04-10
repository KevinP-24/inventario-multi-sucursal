TIPOS_MOVIMIENTO_INVENTARIO_BASE = [
    {
        "nombre": "ENTRADA",
        "descripcion": "Aumenta inventario, por ejemplo al recibir una compra.",
    },
    {
        "nombre": "SALIDA",
        "descripcion": "Disminuye inventario, por ejemplo al confirmar una venta.",
    },
    {
        "nombre": "AJUSTE",
        "descripcion": "Corrige inventario por conteo fisico o ajuste manual.",
    },
    {
        "nombre": "TRANSFERENCIA_ENTRADA",
        "descripcion": "Entrada generada por recibir producto desde otra sucursal.",
    },
    {
        "nombre": "TRANSFERENCIA_SALIDA",
        "descripcion": "Salida generada por enviar producto hacia otra sucursal.",
    },
]


def convertir_tipo_movimiento_inventario_a_respuesta(tipo_movimiento):
    """Convierte un tipo de movimiento SQLAlchemy a diccionario."""
    return tipo_movimiento.convertir_a_diccionario()
