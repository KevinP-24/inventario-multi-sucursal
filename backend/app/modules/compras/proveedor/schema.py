PROVEEDORES_BASE = [
    {
        "nit": "900100200-1",
        "nombre": "Tech Mayoristas SAS",
        "correo": "ventas@techmayoristas.local",
        "telefono": "6011112233",
        "direccion": "Zona industrial tecnologica",
    },
    {
        "nit": "901300400-2",
        "nombre": "Distribuciones Hardware Pro",
        "correo": "contacto@hardwarepro.local",
        "telefono": "6014445566",
        "direccion": "Parque empresarial norte",
    },
]


def validar_datos_para_guardar_proveedor(datos):
    """Valida los datos minimos antes de guardar un proveedor."""
    errores = {}

    if not (datos.get("nit") or "").strip():
        errores["nit"] = "El NIT del proveedor es obligatorio."

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre del proveedor es obligatorio."

    correo = datos.get("correo")
    if correo and "@" not in correo:
        errores["correo"] = "El correo debe tener un formato valido."

    return errores


def convertir_proveedor_a_respuesta(proveedor):
    """Convierte un proveedor SQLAlchemy a diccionario."""
    return proveedor.convertir_a_diccionario()
