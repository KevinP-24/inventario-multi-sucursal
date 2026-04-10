ROLES_BASE = [
    {
        "nombre": "Admin general",
        "descripcion": "Puede administrar todo el sistema y todas las sucursales.",
    },
    {
        "nombre": "Admin sucursal",
        "descripcion": "Administra la operacion de una sucursal especifica.",
    },
    {
        "nombre": "Operario de inventario",
        "descripcion": "Gestiona entradas, salidas y movimientos de inventario.",
    },
]


def validar_datos_para_guardar_rol(datos):
    """Valida lo minimo para crear o editar un rol.

    Lo dejamos simple a proposito: para sustentarlo se puede explicar que aqui
    se revisa lo que llega desde la API antes de tocar la base de datos.
    """
    errores = {}

    nombre = (datos.get("nombre") or "").strip()
    if not nombre:
        errores["nombre"] = "El nombre del rol es obligatorio."

    descripcion = datos.get("descripcion")
    if descripcion is not None and not isinstance(descripcion, str):
        errores["descripcion"] = "La descripcion debe ser texto."

    return errores


def convertir_rol_a_respuesta(rol):
    """Convierte un objeto Rol en un diccionario JSON."""
    return rol.convertir_a_diccionario()
