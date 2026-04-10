from app.modules.logistica.prioridad_ruta_logistica.repository import (
    consultar_prioridad_ruta_logistica_por_id_en_bd,
    consultar_prioridad_ruta_logistica_por_nombre_en_bd,
)
from app.modules.logistica.ruta_logistica.model import RutaLogistica
from app.modules.logistica.ruta_logistica.repository import (
    consultar_cumplimiento_logistico_en_bd,
    consultar_ruta_logistica_por_id_en_bd,
    consultar_ruta_logistica_por_nombre_en_bd,
    consultar_rutas_logistica_clasificadas_en_bd,
    consultar_todas_las_rutas_logistica_en_bd,
    guardar_ruta_logistica_en_base_de_datos,
)
from app.modules.logistica.ruta_logistica.schema import (
    convertir_ruta_logistica_a_respuesta,
    convertir_valor_a_decimal,
    validar_criterio_clasificacion_rutas,
    validar_datos_para_guardar_ruta_logistica,
)


def listar_rutas_logistica_para_respuesta():
    """Consulta rutas logisticas y las deja listas para responder por API."""
    rutas = consultar_todas_las_rutas_logistica_en_bd()
    return [convertir_ruta_logistica_a_respuesta(ruta) for ruta in rutas]


def clasificar_rutas_logistica_para_respuesta(criterio):
    """Lista rutas ordenadas por prioridad, costo o tiempo estimado."""
    criterio_validado, errores = validar_criterio_clasificacion_rutas(criterio)
    if errores:
        return None, errores

    rutas = consultar_rutas_logistica_clasificadas_en_bd(criterio_validado)
    return [convertir_ruta_logistica_a_respuesta(ruta) for ruta in rutas], None


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

    prioridad, errores_prioridad = obtener_prioridad_ruta_para_guardar(datos)
    if errores_prioridad:
        return None, errores_prioridad

    ruta = RutaLogistica(
        nombre_ruta=nombre_ruta,
        id_prioridad_ruta=prioridad.id_prioridad_ruta,
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

    prioridad, errores_prioridad = obtener_prioridad_ruta_para_guardar(datos, ruta)
    if errores_prioridad:
        return None, errores_prioridad

    ruta.nombre_ruta = nombre_ruta
    ruta.id_prioridad_ruta = prioridad.id_prioridad_ruta
    ruta.costo_estimado = convertir_valor_a_decimal(datos.get("costo_estimado", 0))
    ruta.tiempo_estimado = (datos.get("tiempo_estimado") or "").strip() or None

    ruta_guardada = guardar_ruta_logistica_en_base_de_datos(ruta)
    return convertir_ruta_logistica_a_respuesta(ruta_guardada), None


def obtener_prioridad_ruta_para_guardar(datos, ruta_actual=None):
    """Obtiene la prioridad normalizada para crear o actualizar una ruta."""
    if datos.get("id_prioridad_ruta"):
        prioridad = consultar_prioridad_ruta_logistica_por_id_en_bd(datos["id_prioridad_ruta"])
        if not prioridad:
            return None, {"id_prioridad_ruta": "No existe una prioridad de ruta con ese id."}

        return prioridad, None

    nombre_prioridad = (datos.get("prioridad") or "").strip().upper()
    if not nombre_prioridad and ruta_actual:
        prioridad = consultar_prioridad_ruta_logistica_por_id_en_bd(
            ruta_actual.id_prioridad_ruta,
        )
        if prioridad:
            return prioridad, None

    nombre_prioridad = nombre_prioridad or "NORMAL"
    prioridad = consultar_prioridad_ruta_logistica_por_nombre_en_bd(nombre_prioridad)
    if not prioridad:
        return None, {"prioridad": "La prioridad debe existir en el catalogo de rutas."}

    return prioridad, None


def generar_reporte_cumplimiento_logistico_para_respuesta(id_sucursal=None, id_ruta=None):
    """Agrupa cumplimiento de envios por sucursal y ruta."""
    envios = consultar_cumplimiento_logistico_en_bd(id_sucursal, id_ruta)
    resumen = {}

    for envio in envios:
        transferencia = envio.transferencia
        ruta = envio.ruta
        if not transferencia or not ruta:
            continue

        for id_sucursal_transferencia in [
            transferencia.id_sucursal_origen,
            transferencia.id_sucursal_destino,
        ]:
            clave = (id_sucursal_transferencia, ruta.id_ruta)
            if clave not in resumen:
                resumen[clave] = {
                    "id_sucursal": id_sucursal_transferencia,
                    "id_ruta": ruta.id_ruta,
                    "ruta": ruta.nombre_ruta,
                    "total_envios": 0,
                    "entregas_completas": 0,
                    "entregas_parciales": 0,
                    "entregas_a_tiempo": 0,
                    "entregas_tarde": 0,
                    "envios_en_curso": 0,
                }

            item = resumen[clave]
            item["total_envios"] += 1

            if envio.estado_envio == "ENTREGADO":
                item["entregas_completas"] += 1
            elif envio.estado_envio == "ENTREGADO_PARCIAL":
                item["entregas_parciales"] += 1
            else:
                item["envios_en_curso"] += 1

            if envio.fecha_estimada_llegada and envio.fecha_real_llegada:
                if envio.fecha_real_llegada <= envio.fecha_estimada_llegada:
                    item["entregas_a_tiempo"] += 1
                else:
                    item["entregas_tarde"] += 1

    return [
        agregar_porcentaje_cumplimiento(item)
        for item in sorted(resumen.values(), key=lambda item: (item["id_sucursal"], item["ruta"]))
    ]


def agregar_porcentaje_cumplimiento(item):
    """Calcula porcentaje de entregas a tiempo sobre envios ya entregados."""
    entregas_medidas = item["entregas_a_tiempo"] + item["entregas_tarde"]
    item["porcentaje_cumplimiento"] = (
        round((item["entregas_a_tiempo"] / entregas_medidas) * 100, 2)
        if entregas_medidas
        else 0
    )
    return item
