from app.modules.inventario.unidad_medida.model import UnidadMedida
from app.modules.inventario.unidad_medida.repository import (
    consultar_todas_las_unidades_medida_en_bd,
    consultar_unidad_medida_por_id_en_bd,
    consultar_unidad_medida_por_nombre_en_bd,
    consultar_unidad_medida_por_simbolo_en_bd,
    guardar_unidad_medida_en_base_de_datos,
)
from app.modules.inventario.unidad_medida.schema import (
    convertir_unidad_medida_a_respuesta,
    validar_datos_para_guardar_unidad_medida,
)


def listar_unidades_medida_para_respuesta():
    """Consulta unidades de medida y las deja listas para responder por API."""
    unidades = consultar_todas_las_unidades_medida_en_bd()
    return [convertir_unidad_medida_a_respuesta(unidad) for unidad in unidades]


def obtener_unidad_medida_para_respuesta(id_unidad):
    """Consulta una unidad de medida por id y la deja lista para responder."""
    unidad = consultar_unidad_medida_por_id_en_bd(id_unidad)
    if not unidad:
        return None

    return convertir_unidad_medida_a_respuesta(unidad)


def crear_unidad_medida_con_validaciones(datos):
    """Valida datos, evita duplicados y crea la unidad de medida en PostgreSQL."""
    errores = validar_datos_para_guardar_unidad_medida(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    simbolo = datos["simbolo"].strip().lower()

    if consultar_unidad_medida_por_nombre_en_bd(nombre):
        return None, {"nombre": "Ya existe una unidad de medida con ese nombre."}

    if consultar_unidad_medida_por_simbolo_en_bd(simbolo):
        return None, {"simbolo": "Ya existe una unidad de medida con ese simbolo."}

    unidad = UnidadMedida(
        nombre=nombre,
        simbolo=simbolo,
        activo=datos.get("activo", True),
    )

    unidad_guardada = guardar_unidad_medida_en_base_de_datos(unidad)
    return convertir_unidad_medida_a_respuesta(unidad_guardada), None


def actualizar_unidad_medida_con_validaciones(id_unidad, datos):
    """Valida datos y actualiza una unidad de medida existente en PostgreSQL."""
    unidad = consultar_unidad_medida_por_id_en_bd(id_unidad)
    if not unidad:
        return None, {"unidad_medida": "No existe una unidad de medida con ese id."}

    errores = validar_datos_para_guardar_unidad_medida(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    simbolo = datos["simbolo"].strip().lower()

    unidad_con_nombre = consultar_unidad_medida_por_nombre_en_bd(nombre)
    if unidad_con_nombre and unidad_con_nombre.id_unidad != unidad.id_unidad:
        return None, {"nombre": "Ya existe otra unidad de medida con ese nombre."}

    unidad_con_simbolo = consultar_unidad_medida_por_simbolo_en_bd(simbolo)
    if unidad_con_simbolo and unidad_con_simbolo.id_unidad != unidad.id_unidad:
        return None, {"simbolo": "Ya existe otra unidad de medida con ese simbolo."}

    unidad.nombre = nombre
    unidad.simbolo = simbolo
    unidad.activo = datos.get("activo", unidad.activo)

    unidad_guardada = guardar_unidad_medida_en_base_de_datos(unidad)
    return convertir_unidad_medida_a_respuesta(unidad_guardada), None
