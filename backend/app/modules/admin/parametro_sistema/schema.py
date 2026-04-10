PARAMETROS_SISTEMA_BASE = [
    {
        "clave": "NOMBRE_EMPRESA",
        "valor": "MultiSucursal Tech",
        "descripcion": "Nombre usado en la demo del sistema.",
    },
    {
        "clave": "MONEDA_BASE",
        "valor": "COP",
        "descripcion": "Moneda principal para precios y costos.",
    },
    {
        "clave": "PERMITE_STOCK_NEGATIVO",
        "valor": "NO",
        "descripcion": "Controla si inventario puede quedar negativo.",
    },
]


def validar_datos_para_guardar_parametro_sistema(datos):
    """Valida datos minimos antes de guardar un parametro del sistema."""
    errores = {}

    if not (datos.get("clave") or "").strip():
        errores["clave"] = "La clave del parametro es obligatoria."

    if datos.get("valor") is None or str(datos.get("valor")).strip() == "":
        errores["valor"] = "El valor del parametro es obligatorio."

    return errores


def convertir_parametro_sistema_a_respuesta(parametro):
    """Convierte un parametro SQLAlchemy a diccionario."""
    return parametro.convertir_a_diccionario()
