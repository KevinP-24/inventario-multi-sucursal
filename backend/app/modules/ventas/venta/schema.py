from decimal import Decimal, InvalidOperation


ESTADOS_VENTA = ["CONFIRMADA", "ANULADA"]


def convertir_valor_a_decimal(valor):
    """Convierte cantidades y valores monetarios a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_crear_venta(datos):
    """Valida la informacion minima del flujo de registro de venta."""
    errores = {}

    if not datos.get("id_sucursal"):
        errores["id_sucursal"] = "La sucursal es obligatoria."

    if not datos.get("id_usuario"):
        errores["id_usuario"] = "El usuario que registra la venta es obligatorio."

    if not datos.get("id_lista_precio"):
        errores["id_lista_precio"] = "La lista de precios es obligatoria."

    detalles = datos.get("detalles") or []
    if not detalles:
        errores["detalles"] = "La venta necesita al menos un producto."

    for posicion, detalle in enumerate(detalles, start=1):
        validar_detalle_venta(detalle, posicion, errores)

    return errores


def validar_detalle_venta(detalle, posicion, errores):
    """Valida producto, unidad, cantidad y descuento de una linea de venta."""
    prefijo = f"detalle_{posicion}"

    if not detalle.get("id_producto"):
        errores[f"{prefijo}_id_producto"] = "El producto es obligatorio."

    if not detalle.get("id_producto_unidad"):
        errores[f"{prefijo}_id_producto_unidad"] = "La unidad del producto es obligatoria."

    cantidad = convertir_valor_a_decimal(detalle.get("cantidad"))
    if cantidad is None:
        errores[f"{prefijo}_cantidad"] = "La cantidad debe ser numerica."
    elif cantidad <= 0:
        errores[f"{prefijo}_cantidad"] = "La cantidad debe ser mayor a cero."

    descuento = convertir_valor_a_decimal(detalle.get("descuento", 0))
    if descuento is None:
        errores[f"{prefijo}_descuento"] = "El descuento debe ser numerico."
    elif descuento < 0:
        errores[f"{prefijo}_descuento"] = "El descuento no puede ser negativo."


def convertir_venta_a_respuesta(venta):
    """Convierte una venta SQLAlchemy a diccionario para responder por API."""
    return venta.convertir_a_diccionario()
