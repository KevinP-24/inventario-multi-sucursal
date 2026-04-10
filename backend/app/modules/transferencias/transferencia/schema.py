from decimal import Decimal, InvalidOperation


PRIORIDADES_TRANSFERENCIA = ["BAJA", "NORMAL", "ALTA", "URGENTE"]


def convertir_valor_a_decimal(valor):
    """Convierte cantidades a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_crear_transferencia(datos):
    """Valida la solicitud inicial de transferencia entre sucursales."""
    errores = {}

    if not datos.get("id_sucursal_origen"):
        errores["id_sucursal_origen"] = "La sucursal origen es obligatoria."

    if not datos.get("id_sucursal_destino"):
        errores["id_sucursal_destino"] = "La sucursal destino es obligatoria."

    if datos.get("id_sucursal_origen") == datos.get("id_sucursal_destino"):
        errores["sucursales"] = "La sucursal origen y destino deben ser diferentes."

    if not datos.get("id_usuario_solicita"):
        errores["id_usuario_solicita"] = "El usuario que solicita es obligatorio."

    prioridad = (datos.get("prioridad") or "NORMAL").strip().upper()
    if prioridad not in PRIORIDADES_TRANSFERENCIA:
        errores["prioridad"] = "La prioridad debe ser BAJA, NORMAL, ALTA o URGENTE."

    detalles = datos.get("detalles") or []
    if not detalles:
        errores["detalles"] = "La transferencia necesita al menos un producto."

    for posicion, detalle in enumerate(detalles, start=1):
        validar_detalle_solicitud_transferencia(detalle, posicion, errores)

    return errores


def validar_detalle_solicitud_transferencia(detalle, posicion, errores):
    """Valida producto, unidad y cantidad solicitada."""
    prefijo = f"detalle_{posicion}"

    if not detalle.get("id_producto"):
        errores[f"{prefijo}_id_producto"] = "El producto es obligatorio."

    if not detalle.get("id_producto_unidad"):
        errores[f"{prefijo}_id_producto_unidad"] = "La unidad del producto es obligatoria."

    cantidad = convertir_valor_a_decimal(detalle.get("cantidad_solicitada"))
    if cantidad is None:
        errores[f"{prefijo}_cantidad_solicitada"] = "La cantidad solicitada debe ser numerica."
    elif cantidad <= 0:
        errores[f"{prefijo}_cantidad_solicitada"] = "La cantidad solicitada debe ser mayor a cero."


def validar_datos_para_revisar_transferencia(datos):
    """Valida aprobacion, ajuste o rechazo de una transferencia solicitada."""
    errores = {}
    accion = (datos.get("accion") or "").strip().upper()

    if accion not in ["APROBAR", "RECHAZAR"]:
        errores["accion"] = "La accion debe ser APROBAR o RECHAZAR."

    if accion == "APROBAR":
        detalles = datos.get("detalles") or []
        if not detalles:
            errores["detalles"] = "Debe indicar las cantidades aprobadas."

        for posicion, detalle in enumerate(detalles, start=1):
            if not detalle.get("id_detalle_transferencia"):
                errores[f"detalle_{posicion}_id_detalle_transferencia"] = (
                    "El detalle de transferencia es obligatorio."
                )

            cantidad = convertir_valor_a_decimal(detalle.get("cantidad_aprobada"))
            if cantidad is None:
                errores[f"detalle_{posicion}_cantidad_aprobada"] = (
                    "La cantidad aprobada debe ser numerica."
                )
            elif cantidad < 0:
                errores[f"detalle_{posicion}_cantidad_aprobada"] = (
                    "La cantidad aprobada no puede ser negativa."
                )

    return errores


def convertir_transferencia_a_respuesta(transferencia):
    """Convierte una transferencia SQLAlchemy a diccionario."""
    return transferencia.convertir_a_diccionario()
