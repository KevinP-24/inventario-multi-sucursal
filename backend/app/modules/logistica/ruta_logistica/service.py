from app.modules.logistica.ruta_logistica.model import RutaLogistica
from app.modules.logistica.ruta_logistica.repository import (
    consultar_ruta_logistica_por_id_en_bd,
    consultar_ruta_logistica_por_nombre_en_bd,
    consultar_todas_las_rutas_logistica_en_bd,
    guardar_ruta_logistica_en_base_de_datos,
)
from app.modules.logistica.ruta_logistica.schema import (
    convertir_ruta_logistica_a_respuesta,
    convertir_valor_a_decimal,
    validar_datos_para_guardar_ruta_logistica,
)


def listar_rutas_logistica_para_respuesta():
    """Consulta rutas logisticas y las deja listas para responder por API."""
    rutas = consultar_todas_las_rutas_logistica_en_bd()
    return [convertir_ruta_logistica_a_respuesta(ruta) for ruta in rutas]


def obtener_ruta_logistica_para_respuesta(id_ruta):
    """Consulta una ruta logistica por id y la deja lista para responder."""
    ruta = consultar_ruta_logistica_por_id_en_bd(id_ruta)
    if not ruta:
        return None

    return convertir_ruta_logistica_a_respuesta(ruta)


def crear_ruta_logistica_con_validaciones(datos):
    """Valida datos, evita duplicados y crea la ruta logistica."""
    errores = validar_datos_para_guardar_ruta_logistica(datos)
    if errores:
        return None, errores

    nombre_ruta = datos["nombre_ruta"].strip()
    if consultar_ruta_logistica_por_nombre_en_bd(nombre_ruta):
        return None, {"nombre_ruta": "Ya existe una ruta logistica con ese nombre."}

    ruta = RutaLogistica(
        nombre_ruta=nombre_ruta,
        costo_estimado=convertir_valor_a_decimal(datos.get("costo_estimado", 0)),
        tiempo_estimado=(datos.get("tiempo_estimado") or "").strip() or None,
    )

    ruta_guardada = guardar_ruta_logistica_en_base_de_datos(ruta)
    return convertir_ruta_logistica_a_respuesta(ruta_guardada), None


def actualizar_ruta_logistica_con_validaciones(id_ruta, datos):
    """Valida datos y actualiza una ruta logistica existente."""
    ruta = consultar_ruta_logistica_por_id_en_bd(id_ruta)
    if not ruta:
        return None, {"ruta_logistica": "No existe una ruta logistica con ese id."}

    errores = validar_datos_para_guardar_ruta_logistica(datos)
    if errores:
        return None, errores

    nombre_ruta = datos["nombre_ruta"].strip()
    ruta_existente = consultar_ruta_logistica_por_nombre_en_bd(nombre_ruta)
    if ruta_existente and ruta_existente.id_ruta != ruta.id_ruta:
        return None, {"nombre_ruta": "Ya existe otra ruta logistica con ese nombre."}

    ruta.nombre_ruta = nombre_ruta
    ruta.costo_estimado = convertir_valor_a_decimal(datos.get("costo_estimado", 0))
    ruta.tiempo_estimado = (datos.get("tiempo_estimado") or "").strip() or None

    ruta_guardada = guardar_ruta_logistica_en_base_de_datos(ruta)
    return convertir_ruta_logistica_a_respuesta(ruta_guardada), None
