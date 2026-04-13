from datetime import date
from decimal import Decimal, InvalidOperation


PRECIOS_PRODUCTO_BASE = [
    {"codigo_producto": "PROD-001", "lista_precio": "Precio publico", "precio": "55000"},
    {"codigo_producto": "PROD-001", "lista_precio": "Precio corporativo", "precio": "50000"},
    {"codigo_producto": "PROD-002", "lista_precio": "Precio publico", "precio": "180000"},
    {"codigo_producto": "PROD-002", "lista_precio": "Precio corporativo", "precio": "165000"},
    {"codigo_producto": "PROD-003", "lista_precio": "Precio publico", "precio": "620000"},
    {"codigo_producto": "PROD-003", "lista_precio": "Precio corporativo", "precio": "590000"},
]


def convertir_valor_a_decimal(valor):
    """Convierte el precio recibido por API a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def convertir_texto_a_fecha(valor):
    """Convierte una fecha YYYY-MM-DD a date; si no llega, usa hoy."""
    if not valor:
        return date.today()

    return date.fromisoformat(valor)


def validar_datos_para_guardar_precio_producto(datos):
    """Valida datos minimos antes de guardar un precio por producto."""
    errores = {}

    if not datos.get("id_producto"):
        errores["id_producto"] = "El producto es obligatorio."

    if not datos.get("id_lista_precio"):
        errores["id_lista_precio"] = "La lista de precio es obligatoria."

    precio = convertir_valor_a_decimal(datos.get("precio"))
    if precio is None:
        errores["precio"] = "El precio debe ser numerico."
    elif precio <= 0:
        errores["precio"] = "El precio debe ser mayor que cero."

    try:
        convertir_texto_a_fecha(datos.get("fecha_vigencia"))
    except ValueError:
        errores["fecha_vigencia"] = "La fecha debe tener formato YYYY-MM-DD."

    return errores


def convertir_precio_producto_a_respuesta(precio_producto):
    """Convierte un precio-producto SQLAlchemy a diccionario."""
    return precio_producto.convertir_a_diccionario()
