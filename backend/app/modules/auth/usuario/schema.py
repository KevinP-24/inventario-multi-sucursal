def validar_datos_para_guardar_usuario(datos, es_creacion=True):
    """Valida los datos basicos de usuario.

    La idea es que cualquier persona pueda leer estas reglas y entender que
    se exige antes de guardar un usuario en la base de datos.
    """
    errores = {}

    nombre = (datos.get("nombre") or "").strip()
    if not nombre:
        errores["nombre"] = "El nombre del usuario es obligatorio."

    correo = (datos.get("correo") or "").strip().lower()
    if not correo:
        errores["correo"] = "El correo es obligatorio."
    elif "@" not in correo:
        errores["correo"] = "El correo debe tener un formato valido."

    if not datos.get("id_rol"):
        errores["id_rol"] = "El usuario debe tener un rol."

    password = datos.get("password")
    if es_creacion and not password:
        errores["password"] = "La contrasena es obligatoria al crear el usuario."
    elif password and len(password) < 6:
        errores["password"] = "La contrasena debe tener minimo 6 caracteres."

    return errores


def convertir_usuario_a_respuesta(usuario):
    """Convierte el usuario en un diccionario seguro para responder por API."""
    return usuario.convertir_a_diccionario()
