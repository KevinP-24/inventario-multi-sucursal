from decimal import Decimal, InvalidOperation

RUTAS_LOGISTICA_BASE = [
    {
        "nombre_ruta": "Centro Tecnologico - Norte Empresarial",
        "prioridad": "ALTA",
        "costo_estimado": "25000",
        "tiempo_estimado": "45 minutos",
    },
    {
        "nombre_ruta": "Centro Tecnologico - Outlet Sur",
        "prioridad": "NORMAL",
        "costo_estimado": "30000",
        "tiempo_estimado": "60 minutos",
    },
]


def convertir_valor_a_decimal(valor):
    """Convierte el costo recibido por API a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_guardar_ruta_logistica(datos):
    """Valida datos minimos antes de guardar una ruta logistica."""
    errores = {}

    if not (datos.get("nombre_ruta") or "").strip():
        errores["nombre_ruta"] = "El nombre de la ruta es obligatorio."

    if datos.get("id_prioridad_ruta") and datos.get("prioridad"):
        errores["prioridad"] = "Envie id_prioridad_ruta o prioridad, no ambos."

    costo_estimado = convertir_valor_a_decimal(datos.get("costo_estimado", 0))
    if costo_estimado is None:
        errores["costo_estimado"] = "El costo estimado debe ser numerico."
    elif costo_estimado < 0:
        errores["costo_estimado"] = "El costo estimado no puede ser negativo."

    return errores


def validar_criterio_clasificacion_rutas(criterio):
    """Valida el criterio usado para ordenar rutas logisticas."""
    criterio_normalizado = (criterio or "prioridad").strip().lower()
    if criterio_normalizado not in ["prioridad", "costo", "tiempo"]:
        return None, {"criterio": "El criterio debe ser prioridad, costo o tiempo."}

    return criterio_normalizado, None


def convertir_ruta_logistica_a_respuesta(ruta_logistica):
    """Convierte una ruta logistica SQLAlchemy a diccionario."""
    return ruta_logistica.convertir_a_diccionario()
