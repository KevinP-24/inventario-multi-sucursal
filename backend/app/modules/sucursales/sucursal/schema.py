SUCURSALES_BASE = [
    {
        "nombre": "Sucursal Centro Tecnologico",
        "direccion": "Calle 10 # 15-20 Local 201",
        "ciudad": "Bogota",
        "telefono": "6010000001",
        "estado": "activa",
    },
    {
        "nombre": "Sucursal Norte Empresarial",
        "direccion": "Carrera 45 # 120-10 Oficina 304",
        "ciudad": "Bogota",
        "telefono": "6010000002",
        "estado": "activa",
    },
    {
        "nombre": "Sucursal Outlet Sur",
        "direccion": "Avenida 1 # 30-50 Bodega 8",
        "ciudad": "Bogota",
        "telefono": "6010000003",
        "estado": "activa",
    },
]


def validar_datos_para_guardar_sucursal(datos):
    """Valida los datos minimos antes de guardar una sucursal."""
    errores = {}

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre de la sucursal es obligatorio."

    if not (datos.get("direccion") or "").strip():
        errores["direccion"] = "La direccion de la sucursal es obligatoria."

    if not (datos.get("ciudad") or "").strip():
        errores["ciudad"] = "La ciudad de la sucursal es obligatoria."

    estado = (datos.get("estado") or "activa").strip().lower()
    if estado not in ["activa", "inactiva"]:
        errores["estado"] = "El estado debe ser activa o inactiva."

    return errores


def convertir_sucursal_a_respuesta(sucursal):
    """Convierte una sucursal SQLAlchemy a diccionario."""
    return sucursal.convertir_a_diccionario()
