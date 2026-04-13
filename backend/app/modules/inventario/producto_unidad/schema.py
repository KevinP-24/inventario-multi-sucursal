from decimal import Decimal, InvalidOperation


PRODUCTO_UNIDADES_BASE = [
    {"codigo_producto": "PROD-001", "simbolo_unidad": "und", "factor_conversion": "1", "es_base": True},
    {"codigo_producto": "PROD-002", "simbolo_unidad": "und", "factor_conversion": "1", "es_base": True},
    {"codigo_producto": "PROD-003", "simbolo_unidad": "und", "factor_conversion": "1", "es_base": True},
    {"codigo_producto": "PROD-004", "simbolo_unidad": "lt", "factor_conversion": "1", "es_base": True},
    {"codigo_producto": "PROD-005", "simbolo_unidad": "g", "factor_conversion": "1", "es_base": True},
    {"codigo_producto": "PROD-006", "simbolo_unidad": "m", "factor_conversion": "2", "es_base": True},
    {"codigo_producto": "PROD-001", "simbolo_unidad": "cja", "factor_conversion": "20", "es_base": False},
    {"codigo_producto": "PROD-002", "simbolo_unidad": "cja", "factor_conversion": "10", "es_base": False},
]


def convertir_valor_a_decimal(valor):
    """Convierte el factor recibido por API a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_guardar_producto_unidad(datos):
    """Valida datos minimos antes de guardar una conversion producto-unidad."""
    errores = {}

    if not datos.get("id_producto"):
        errores["id_producto"] = "El producto es obligatorio."

    if not datos.get("id_unidad"):
        errores["id_unidad"] = "La unidad de medida es obligatoria."

    factor_conversion = convertir_valor_a_decimal(datos.get("factor_conversion", 1))
    if factor_conversion is None:
        errores["factor_conversion"] = "El factor de conversion debe ser numerico."
    elif factor_conversion <= 0:
        errores["factor_conversion"] = "El factor de conversion debe ser mayor que cero."

    return errores


def convertir_producto_unidad_a_respuesta(producto_unidad):
    """Convierte una relacion producto-unidad SQLAlchemy a diccionario."""
    return producto_unidad.convertir_a_diccionario()
