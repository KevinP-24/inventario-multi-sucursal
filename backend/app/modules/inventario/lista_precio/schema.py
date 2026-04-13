LISTAS_PRECIO_BASE = [
    {
        "nombre": "Precio publico",
        "descripcion": "Precio normal para ventas de mostrador.",
    },
    {
        "nombre": "Precio corporativo",
        "descripcion": "Precio para clientes empresariales o compras recurrentes.",
    },
]


def validar_datos_para_guardar_lista_precio(datos):
    """Valida los datos minimos antes de guardar una lista de precio."""
    errores = {}

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre de la lista de precio es obligatorio."

    return errores


def convertir_lista_precio_a_respuesta(lista_precio):
    """Convierte una lista de precio SQLAlchemy a diccionario."""
    return lista_precio.convertir_a_diccionario()
