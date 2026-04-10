from decimal import Decimal, InvalidOperation


TRATAMIENTOS_INCIDENCIA = ["REENVIO", "AJUSTE", "RECLAMACION"]


def convertir_valor_a_decimal(valor):
    """Convierte cantidades recibidas a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_confirmar_recepcion_transferencia(datos):
    """Valida cantidades recibidas y tratamiento de diferencias."""
    errores = {}

    if not datos.get("id_usuario_recibe"):
        errores["id_usuario_recibe"] = "El usuario que recibe es obligatorio."

    detalles = datos.get("detalles") or []
    if not detalles:
        errores["detalles"] = "Debe indicar las cantidades recibidas."

    for posicion, detalle in enumerate(detalles, start=1):
        prefijo = f"detalle_{posicion}"

        if not detalle.get("id_detalle_transferencia"):
            errores[f"{prefijo}_id_detalle_transferencia"] = "El detalle es obligatorio."

        cantidad = convertir_valor_a_decimal(detalle.get("cantidad_recibida"))
        if cantidad is None:
            errores[f"{prefijo}_cantidad_recibida"] = "La cantidad recibida debe ser numerica."
        elif cantidad < 0:
            errores[f"{prefijo}_cantidad_recibida"] = "La cantidad recibida no puede ser negativa."

        tratamiento = (detalle.get("tratamiento") or "").strip().upper()
        if tratamiento and tratamiento not in TRATAMIENTOS_INCIDENCIA:
            errores[f"{prefijo}_tratamiento"] = (
                "El tratamiento debe ser REENVIO, AJUSTE o RECLAMACION."
            )

    return errores


def convertir_recepcion_transferencia_a_respuesta(recepcion):
    """Convierte una recepcion SQLAlchemy a diccionario."""
    return recepcion.convertir_a_diccionario()
