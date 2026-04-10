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


def validar_datos_para_ajustar_inventario_sucursal(datos):
    """Valida una entrada, salida o ajuste manual de stock.

    ENTRADA y SALIDA trabajan con una cantidad de movimiento. AJUSTE fija la
    cantidad actual nueva, como ocurre despues de un conteo fisico.
    """
    errores = {}
    tipo_ajuste = (datos.get("tipo_ajuste") or "").strip().upper()

    if not datos.get("id_usuario"):
        errores["id_usuario"] = "El usuario responsable es obligatorio."

    if tipo_ajuste not in ["ENTRADA", "SALIDA", "AJUSTE"]:
        errores["tipo_ajuste"] = "El tipo de ajuste debe ser ENTRADA, SALIDA o AJUSTE."

    if tipo_ajuste in ["ENTRADA", "SALIDA"]:
        cantidad = convertir_valor_a_decimal(datos.get("cantidad"))
        if cantidad is None:
            errores["cantidad"] = "La cantidad debe ser numerica."
        elif cantidad <= 0:
            errores["cantidad"] = "La cantidad debe ser mayor a cero."

    if tipo_ajuste == "AJUSTE":
        cantidad_actual_nueva = convertir_valor_a_decimal(datos.get("cantidad_actual_nueva"))
        if cantidad_actual_nueva is None:
            errores["cantidad_actual_nueva"] = "La cantidad actual nueva debe ser numerica."
        elif cantidad_actual_nueva < 0:
            errores["cantidad_actual_nueva"] = "La cantidad actual nueva no puede ser negativa."

    return errores


def validar_datos_para_movimiento_operativo_inventario(datos):
    """Valida devoluciones y mermas, que siempre mueven una cantidad concreta."""
    errores = {}

    if not datos.get("id_usuario"):
        errores["id_usuario"] = "El usuario responsable es obligatorio."

    cantidad = convertir_valor_a_decimal(datos.get("cantidad"))
    if cantidad is None:
        errores["cantidad"] = "La cantidad debe ser numerica."
    elif cantidad <= 0:
        errores["cantidad"] = "La cantidad debe ser mayor a cero."

    id_origen = datos.get("id_origen")
    if id_origen is not None:
        try:
            int(id_origen)
        except (TypeError, ValueError):
            errores["id_origen"] = "El id de origen debe ser numerico si se envia."

    return errores


def convertir_inventario_sucursal_a_respuesta(inventario):
    """Convierte un registro SQLAlchemy a diccionario para responder por API."""
    return inventario.convertir_a_diccionario()


def convertir_alerta_stock_bajo_a_respuesta(inventario):
    """Convierte un inventario bajo minimo en una alerta sencilla para API."""
    producto = inventario.producto
    return {
        "id_inventario": inventario.id_inventario,
        "id_sucursal": inventario.id_sucursal,
        "id_producto": inventario.id_producto,
        "producto": producto.nombre if producto else None,
        "codigo_producto": producto.codigo if producto else None,
        "cantidad_actual": float(inventario.cantidad_actual),
        "stock_minimo": float(producto.stock_minimo) if producto else 0,
        "cantidad_faltante": (
            float(producto.stock_minimo - inventario.cantidad_actual) if producto else 0
        ),
    }
