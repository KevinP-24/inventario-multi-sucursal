from app.modules.logistica.transportista.model import Transportista
from app.modules.logistica.transportista.repository import (
    consultar_todos_los_transportistas_en_bd,
    consultar_transportista_por_id_en_bd,
    consultar_transportista_por_identificacion_en_bd,
    guardar_transportista_en_base_de_datos,
)
from app.modules.logistica.transportista.schema import (
    convertir_transportista_a_respuesta,
    validar_datos_para_guardar_transportista,
)


def listar_transportistas_para_respuesta():
    """Consulta transportistas y los deja listos para responder por API."""
    transportistas = consultar_todos_los_transportistas_en_bd()
    return [convertir_transportista_a_respuesta(transportista) for transportista in transportistas]


def obtener_transportista_para_respuesta(id_transportista):
    """Consulta un transportista por id y lo deja listo para responder."""
    transportista = consultar_transportista_por_id_en_bd(id_transportista)
    if not transportista:
        return None

    return convertir_transportista_a_respuesta(transportista)


def crear_transportista_con_validaciones(datos):
    """Valida datos, evita duplicados y crea el transportista."""
    errores = validar_datos_para_guardar_transportista(datos)
    if errores:
        return None, errores

    identificacion = datos["identificacion"].strip()
    if consultar_transportista_por_identificacion_en_bd(identificacion):
        return None, {"identificacion": "Ya existe un transportista con esa identificacion."}

    transportista = Transportista(
        identificacion=identificacion,
        nombre=datos["nombre"].strip(),
        telefono=(datos.get("telefono") or "").strip() or None,
        activo=datos.get("activo", True),
    )

    transportista_guardado = guardar_transportista_en_base_de_datos(transportista)
    return convertir_transportista_a_respuesta(transportista_guardado), None


def actualizar_transportista_con_validaciones(id_transportista, datos):
    """Valida datos y actualiza un transportista existente."""
    transportista = consultar_transportista_por_id_en_bd(id_transportista)
    if not transportista:
        return None, {"transportista": "No existe un transportista con ese id."}

    errores = validar_datos_para_guardar_transportista(datos)
    if errores:
        return None, errores

    identificacion = datos["identificacion"].strip()
    existente = consultar_transportista_por_identificacion_en_bd(identificacion)
    if existente and existente.id_transportista != transportista.id_transportista:
        return None, {"identificacion": "Ya existe otro transportista con esa identificacion."}

    transportista.identificacion = identificacion
    transportista.nombre = datos["nombre"].strip()
    transportista.telefono = (datos.get("telefono") or "").strip() or None
    transportista.activo = datos.get("activo", transportista.activo)

    transportista_guardado = guardar_transportista_en_base_de_datos(transportista)
    return convertir_transportista_a_respuesta(transportista_guardado), None
