def validar_datos_para_guardar_cliente(datos):
    """Valida lo minimo para crear o actualizar un cliente."""
    errores = {}

    if not (datos.get("tipo_documento") or "").strip():
        errores["tipo_documento"] = "El tipo de documento es obligatorio."

    if not (datos.get("numero_documento") or "").strip():
        errores["numero_documento"] = "El numero de documento es obligatorio."

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre del cliente es obligatorio."

    correo = datos.get("correo")
    if correo and "@" not in correo:
        errores["correo"] = "El correo debe tener un formato valido."

    return errores


def convertir_cliente_a_respuesta(cliente):
    """Convierte un cliente SQLAlchemy a diccionario."""
    return cliente.convertir_a_diccionario()
