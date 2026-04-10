from decimal import Decimal, InvalidOperation


INVENTARIO_SUCURSAL_BASE = [
    {
        "sucursal": "Sucursal Centro Tecnologico",
        "producto": "PROD-001",
        "cantidad_actual": "25",
        "costo_promedio": "42000",
    },
    {
        "sucursal": "Sucursal Centro Tecnologico",
        "producto": "PROD-002",
        "cantidad_actual": "12",
        "costo_promedio": "135000",
    },
    {
        "sucursal": "Sucursal Norte Empresarial",
        "producto": "PROD-003",
        "cantidad_actual": "8",
        "costo_promedio": "520000",
    },
    {
        "sucursal": "Sucursal Outlet Sur",
        "producto": "PROD-006",
        "cantidad_actual": "40",
        "costo_promedio": "18000",
    },
]


def convertir_valor_a_decimal(valor):
    """Convierte cantidades o costos a Decimal para guardar en PostgreSQL."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_guardar_inventario_sucursal(datos):
    """Valida los datos minimos del stock por sucursal y producto."""
    errores = {}

    if not datos.get("id_sucursal"):
        errores["id_sucursal"] = "La sucursal es obligatoria."

    if not datos.get("id_producto"):
        errores["id_producto"] = "El producto es obligatorio."

    cantidad_actual = convertir_valor_a_decimal(datos.get("cantidad_actual", 0))
    if cantidad_actual is None:
        errores["cantidad_actual"] = "La cantidad actual debe ser numerica."
    elif cantidad_actual < 0:
        errores["cantidad_actual"] = "La cantidad actual no puede ser negativa."

    costo_promedio = convertir_valor_a_decimal(datos.get("costo_promedio", 0))
    if costo_promedio is None:
        errores["costo_promedio"] = "El costo promedio debe ser numerico."
    elif costo_promedio < 0:
        errores["costo_promedio"] = "El costo promedio no puede ser negativo."

    return errores


def convertir_inventario_sucursal_a_respuesta(inventario):
    """Convierte un registro SQLAlchemy a diccionario para responder por API."""
    return inventario.convertir_a_diccionario()
