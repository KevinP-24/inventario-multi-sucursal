PROVEEDORES_BASE = [
    {
        "codigo_tipo_documento": "NIT",
        "numero_documento": "900100200-1",
        "nombre": "Tech Mayoristas SAS",
        "correo": "ventas@techmayoristas.local",
        "telefono": "6011112233",
        "direccion": "Zona industrial tecnologica",
    },
    {
        "codigo_tipo_documento": "NIT",
        "numero_documento": "901300400-2",
        "nombre": "Distribuciones Hardware Pro",
        "correo": "contacto@hardwarepro.local",
        "telefono": "6014445566",
        "direccion": "Parque empresarial norte",
    },
]


def validar_datos_para_guardar_proveedor(datos):
    """Valida los datos minimos antes de guardar un proveedor."""
    errores = {}

    if not datos.get("id_tipo_documento"):
        errores["id_tipo_documento"] = "El tipo de documento del proveedor es obligatorio."

    if not (datos.get("numero_documento") or "").strip():
        errores["numero_documento"] = "El numero de documento del proveedor es obligatorio."

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre del proveedor es obligatorio."

    correo = datos.get("correo")
    if correo and "@" not in correo:
        errores["correo"] = "El correo debe tener un formato valido."

    return errores



def convertir_proveedor_a_respuesta(proveedor):
    """Convierte un proveedor SQLAlchemy a diccionario."""
    return proveedor.convertir_a_diccionario()
