from datetime import datetime
from decimal import Decimal, InvalidOperation


def convertir_valor_a_decimal(valor):
    """Convierte la cantidad recibida por API a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def convertir_texto_a_fecha_hora(valor):
    """Convierte fecha_hora ISO a datetime; si viene vacia, usa la hora actual."""
    if not valor:
        return datetime.utcnow()

    try:
        return datetime.fromisoformat(str(valor))
    except ValueError:
        return None


def convertir_texto_a_fecha_hora_para_filtro(valor, es_fecha_hasta=False):
    """Convierte filtros de fecha ISO; acepta YYYY-MM-DD o fecha/hora completa."""
    if not valor:
        return None

    texto = str(valor).strip()
    try:
        if len(texto) == 10:
            sufijo = "T23:59:59" if es_fecha_hasta else "T00:00:00"
            texto = f"{texto}{sufijo}"
        return datetime.fromisoformat(texto)
    except ValueError:
        return None


def validar_datos_para_registrar_movimiento_inventario(datos):
    """Valida los datos minimos para dejar trazabilidad del inventario."""
    errores = {}

    if not datos.get("id_inventario"):
        errores["id_inventario"] = "El inventario es obligatorio."

    if not datos.get("id_usuario"):
        errores["id_usuario"] = "El usuario es obligatorio."

    if not datos.get("id_tipo_movimiento"):
        errores["id_tipo_movimiento"] = "El tipo de movimiento es obligatorio."

    cantidad = convertir_valor_a_decimal(datos.get("cantidad"))
    if cantidad is None:
        errores["cantidad"] = "La cantidad debe ser numerica."
    elif cantidad <= 0:
        errores["cantidad"] = "La cantidad debe ser mayor a cero."

    fecha_hora = convertir_texto_a_fecha_hora(datos.get("fecha_hora"))
    if fecha_hora is None:
        errores["fecha_hora"] = "La fecha debe venir en formato ISO, por ejemplo 2026-04-10T08:30:00."

    return errores


def convertir_movimiento_inventario_a_respuesta(movimiento):
    """Convierte un movimiento SQLAlchemy a diccionario para responder por API."""
    return movimiento.convertir_a_diccionario()
