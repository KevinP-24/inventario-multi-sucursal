from app.modules.sucursales.sucursal.model import Sucursal
from app.modules.sucursales.sucursal.repository import (
    consultar_sucursal_por_id_en_bd,
    consultar_sucursal_por_nombre_en_bd,
    consultar_todas_las_sucursales_en_bd,
    guardar_sucursal_en_base_de_datos,
)
from app.modules.sucursales.sucursal.schema import (
    convertir_sucursal_a_respuesta,
    validar_datos_para_guardar_sucursal,
)


def listar_sucursales_para_respuesta():
    """Consulta sucursales y las deja listas para responder por la API."""
    sucursales = consultar_todas_las_sucursales_en_bd()
    return [convertir_sucursal_a_respuesta(sucursal) for sucursal in sucursales]


def obtener_sucursal_para_respuesta(id_sucursal):
    """Consulta una sucursal por id y la deja lista para responder por la API."""
    sucursal = consultar_sucursal_por_id_en_bd(id_sucursal)
    if not sucursal:
        return None

    return convertir_sucursal_a_respuesta(sucursal)


def crear_sucursal_con_validaciones(datos):
    """Valida datos, evita duplicados y crea la sucursal en PostgreSQL."""
    errores = validar_datos_para_guardar_sucursal(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    if consultar_sucursal_por_nombre_en_bd(nombre):
        return None, {"nombre": "Ya existe una sucursal con ese nombre."}

    sucursal = Sucursal(
        nombre=nombre,
        direccion=datos["direccion"].strip(),
        ciudad=datos["ciudad"].strip(),
        telefono=(datos.get("telefono") or "").strip() or None,
        estado=(datos.get("estado") or "activa").strip().lower(),
    )

    sucursal_guardada = guardar_sucursal_en_base_de_datos(sucursal)
    return convertir_sucursal_a_respuesta(sucursal_guardada), None


def actualizar_sucursal_con_validaciones(id_sucursal, datos):
    """Valida datos y actualiza una sucursal existente en PostgreSQL."""
    sucursal = consultar_sucursal_por_id_en_bd(id_sucursal)
    if not sucursal:
        return None, {"sucursal": "No existe una sucursal con ese id."}

    errores = validar_datos_para_guardar_sucursal(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    sucursal_existente = consultar_sucursal_por_nombre_en_bd(nombre)
    if sucursal_existente and sucursal_existente.id_sucursal != sucursal.id_sucursal:
        return None, {"nombre": "Ya existe otra sucursal con ese nombre."}

    sucursal.nombre = nombre
    sucursal.direccion = datos["direccion"].strip()
    sucursal.ciudad = datos["ciudad"].strip()
    sucursal.telefono = (datos.get("telefono") or "").strip() or None
    sucursal.estado = (datos.get("estado") or sucursal.estado).strip().lower()

    sucursal_guardada = guardar_sucursal_en_base_de_datos(sucursal)
    return convertir_sucursal_a_respuesta(sucursal_guardada), None
