from app.modules.admin.parametro_sistema.model import ParametroSistema
from app.modules.admin.parametro_sistema.repository import (
    consultar_parametro_sistema_por_clave_en_bd,
    consultar_parametro_sistema_por_id_en_bd,
    consultar_todos_los_parametros_sistema_en_bd,
    guardar_parametro_sistema_en_base_de_datos,
)
from app.modules.admin.parametro_sistema.schema import (
    convertir_parametro_sistema_a_respuesta,
    validar_datos_para_guardar_parametro_sistema,
)


def listar_parametros_sistema_para_respuesta():
    """Consulta parametros y los deja listos para responder por API."""
    parametros = consultar_todos_los_parametros_sistema_en_bd()
    return [convertir_parametro_sistema_a_respuesta(parametro) for parametro in parametros]


def obtener_parametro_sistema_para_respuesta(id_parametro):
    """Consulta un parametro por id y lo deja listo para responder."""
    parametro = consultar_parametro_sistema_por_id_en_bd(id_parametro)
    if not parametro:
        return None

    return convertir_parametro_sistema_a_respuesta(parametro)


def crear_parametro_sistema_con_validaciones(datos):
    """Valida datos, evita claves duplicadas y crea el parametro."""
    errores = validar_datos_para_guardar_parametro_sistema(datos)
    if errores:
        return None, errores

    clave = datos["clave"].strip().upper()
    if consultar_parametro_sistema_por_clave_en_bd(clave):
        return None, {"clave": "Ya existe un parametro con esa clave."}

    parametro = ParametroSistema(
        clave=clave,
        valor=str(datos["valor"]).strip(),
        descripcion=(datos.get("descripcion") or "").strip() or None,
        activo=datos.get("activo", True),
    )

    parametro_guardado = guardar_parametro_sistema_en_base_de_datos(parametro)
    return convertir_parametro_sistema_a_respuesta(parametro_guardado), None


def actualizar_parametro_sistema_con_validaciones(id_parametro, datos):
    """Valida datos y actualiza un parametro existente."""
    parametro = consultar_parametro_sistema_por_id_en_bd(id_parametro)
    if not parametro:
        return None, {"parametro": "No existe un parametro con ese id."}

    errores = validar_datos_para_guardar_parametro_sistema(datos)
    if errores:
        return None, errores

    clave = datos["clave"].strip().upper()
    existente = consultar_parametro_sistema_por_clave_en_bd(clave)
    if existente and existente.id_parametro != parametro.id_parametro:
        return None, {"clave": "Ya existe otro parametro con esa clave."}

    parametro.clave = clave
    parametro.valor = str(datos["valor"]).strip()
    parametro.descripcion = (datos.get("descripcion") or "").strip() or None
    parametro.activo = datos.get("activo", parametro.activo)

    parametro_guardado = guardar_parametro_sistema_en_base_de_datos(parametro)
    return convertir_parametro_sistema_a_respuesta(parametro_guardado), None
