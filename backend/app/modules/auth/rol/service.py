from app.modules.auth.rol.model import Rol
from app.modules.auth.rol.repository import (
    consultar_rol_por_id_en_bd,
    consultar_rol_por_nombre_en_bd,
    consultar_todos_los_roles_en_bd,
    guardar_rol_en_base_de_datos,
)
from app.modules.auth.rol.schema import (
    ROLES_BASE,
    convertir_rol_a_respuesta,
    validar_datos_para_guardar_rol,
)


def listar_roles_para_respuesta():
    """Consulta los roles y los deja listos para responder por la API."""
    roles = consultar_todos_los_roles_en_bd()
    return [convertir_rol_a_respuesta(rol) for rol in roles]


def obtener_rol_para_respuesta(id_rol):
    """Consulta un rol por id y lo deja listo para responder por la API."""
    rol = consultar_rol_por_id_en_bd(id_rol)
    if not rol:
        return None

    return convertir_rol_a_respuesta(rol)


def crear_rol_con_validaciones(datos):
    """Valida los datos, evita duplicados y crea el rol en PostgreSQL."""
    errores = validar_datos_para_guardar_rol(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    if consultar_rol_por_nombre_en_bd(nombre):
        return None, {"nombre": "Ya existe un rol con ese nombre."}

    rol = Rol(
        nombre=nombre,
        descripcion=datos.get("descripcion"),
        activo=datos.get("activo", True),
    )

    rol_guardado = guardar_rol_en_base_de_datos(rol)
    return convertir_rol_a_respuesta(rol_guardado), None


def actualizar_rol_con_validaciones(id_rol, datos):
    """Valida los datos y actualiza un rol existente en PostgreSQL."""
    rol = consultar_rol_por_id_en_bd(id_rol)
    if not rol:
        return None, {"rol": "No existe un rol con ese id."}

    errores = validar_datos_para_guardar_rol(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    rol_existente = consultar_rol_por_nombre_en_bd(nombre)
    if rol_existente and rol_existente.id_rol != rol.id_rol:
        return None, {"nombre": "Ya existe otro rol con ese nombre."}

    rol.nombre = nombre
    rol.descripcion = datos.get("descripcion")
    rol.activo = datos.get("activo", rol.activo)

    rol_guardado = guardar_rol_en_base_de_datos(rol)
    return convertir_rol_a_respuesta(rol_guardado), None


def crear_roles_base_si_no_existen():
    """Crea los roles principales del sistema si todavia no existen.

    Esto ayuda a la sustentacion porque deja claro cuales son los actores:
    Admin general, Admin sucursal y Operario de inventario.
    """
    roles_creados = []

    for datos_rol in ROLES_BASE:
        rol = consultar_rol_por_nombre_en_bd(datos_rol["nombre"])
        if not rol:
            rol = Rol(**datos_rol)
            guardar_rol_en_base_de_datos(rol)

        roles_creados.append(convertir_rol_a_respuesta(rol))

    return roles_creados
