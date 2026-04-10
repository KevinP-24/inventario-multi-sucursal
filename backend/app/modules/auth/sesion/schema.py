def validar_datos_login(datos):
    """Valida credenciales minimas para iniciar sesion."""
    errores = {}

    correo = (datos.get("correo") or "").strip().lower()
    if not correo:
        errores["correo"] = "El correo es obligatorio."
    elif "@" not in correo:
        errores["correo"] = "El correo debe tener un formato valido."

    if not datos.get("password"):
        errores["password"] = "La contrasena es obligatoria."

    return errores
