from datetime import datetime


def convertir_texto_a_fecha_hora(valor):
    """Convierte texto ISO a datetime; si viene vacio, devuelve None."""
    if not valor:
        return None

    try:
        return datetime.fromisoformat(str(valor))
    except ValueError:
        return None


def validar_datos_para_registrar_envio_transferencia(datos):
    """Valida la informacion basica del despacho de una transferencia."""
    errores = {}

    if not datos.get("id_ruta"):
        errores["id_ruta"] = "La ruta logistica es obligatoria."

    if not datos.get("id_transportista"):
        errores["id_transportista"] = "El transportista es obligatorio."

    fecha_estimada = datos.get("fecha_estimada_llegada")
    if fecha_estimada and convertir_texto_a_fecha_hora(fecha_estimada) is None:
        errores["fecha_estimada_llegada"] = "La fecha estimada debe tener formato ISO."

    return errores


def convertir_envio_transferencia_a_respuesta(envio):
    """Convierte un envio SQLAlchemy a diccionario."""
    return envio.convertir_a_diccionario()
