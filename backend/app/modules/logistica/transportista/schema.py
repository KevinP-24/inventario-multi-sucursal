TRANSPORTISTAS_BASE = [
    {
        "identificacion": "TRANS-001",
        "nombre": "Logistica Rapida Tech",
        "telefono": "3001112233",
    },
    {
        "identificacion": "TRANS-002",
        "nombre": "Mensajeria Empresarial Norte",
        "telefono": "3004445566",
    },
]


def validar_datos_para_guardar_transportista(datos):
    """Valida datos minimos antes de guardar un transportista."""
    errores = {}

    if not (datos.get("identificacion") or "").strip():
        errores["identificacion"] = "La identificacion del transportista es obligatoria."

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre del transportista es obligatorio."

    return errores


def convertir_transportista_a_respuesta(transportista):
    """Convierte un transportista SQLAlchemy a diccionario."""
    return transportista.convertir_a_diccionario()
