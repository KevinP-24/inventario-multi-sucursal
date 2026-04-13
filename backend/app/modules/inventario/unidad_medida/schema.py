UNIDADES_MEDIDA_BASE = [
    {"nombre": "Unidad", "simbolo": "und"},
    {"nombre": "Caja", "simbolo": "cja"},
    {"nombre": "Litro", "simbolo": "lt"},
    {"nombre": "Gramo", "simbolo": "g"},
    {"nombre": "Metro", "simbolo": "m"},
    {"nombre": "Paquete", "simbolo": "paq"},
]


def validar_datos_para_guardar_unidad_medida(datos):
    """Valida los datos minimos antes de guardar una unidad de medida."""
    errores = {}

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre de la unidad de medida es obligatorio."

    if not (datos.get("simbolo") or "").strip():
        errores["simbolo"] = "El simbolo de la unidad de medida es obligatorio."

    return errores


def convertir_unidad_medida_a_respuesta(unidad_medida):
    """Convierte una unidad de medida SQLAlchemy a diccionario."""
    return unidad_medida.convertir_a_diccionario()
