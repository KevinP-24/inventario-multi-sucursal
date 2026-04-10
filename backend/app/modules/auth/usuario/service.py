from app.modules.auth.rol.repository import consultar_rol_por_id_en_bd
from app.modules.sucursales.sucursal.repository import consultar_sucursal_por_id_en_bd
from app.modules.auth.usuario.model import Usuario
from app.modules.auth.usuario.repository import (
    consultar_todos_los_usuarios_en_bd,
    consultar_usuario_por_correo_en_bd,
    consultar_usuario_por_id_en_bd,
    guardar_usuario_en_base_de_datos,
)
from app.modules.auth.usuario.schema import (
    convertir_usuario_a_respuesta,
    validar_datos_para_guardar_usuario,
)
from app.security.password import generar_hash_password


def listar_usuarios_para_respuesta():
    """Consulta usuarios y los deja listos para responder sin contrasena."""
    usuarios = consultar_todos_los_usuarios_en_bd()
    return [convertir_usuario_a_respuesta(usuario) for usuario in usuarios]


def obtener_usuario_para_respuesta(id_usuario):
    """Consulta un usuario por id y lo deja listo para responder por la API."""
    usuario = consultar_usuario_por_id_en_bd(id_usuario)
    if not usuario:
        return None

    return convertir_usuario_a_respuesta(usuario)


def crear_usuario_con_validaciones(datos):
    """Valida datos, revisa rol/correo y crea el usuario en PostgreSQL."""
    errores = validar_datos_para_guardar_usuario(datos, es_creacion=True)
    if errores:
        return None, errores

    correo = datos["correo"].strip().lower()
    if consultar_usuario_por_correo_en_bd(correo):
        return None, {"correo": "Ya existe un usuario con ese correo."}

    rol = consultar_rol_por_id_en_bd(datos["id_rol"])
    if not rol:
        return None, {"id_rol": "El rol indicado no existe."}

    id_sucursal = datos.get("id_sucursal")
    if id_sucursal and not consultar_sucursal_por_id_en_bd(id_sucursal):
        return None, {"id_sucursal": "La sucursal indicada no existe."}

    usuario = Usuario(
        id_rol=datos["id_rol"],
        id_sucursal=id_sucursal,
        nombre=datos["nombre"].strip(),
        correo=correo,
        password_hash=generar_hash_password(datos["password"]),
        activo=datos.get("activo", True),
    )

    usuario_guardado = guardar_usuario_en_base_de_datos(usuario)
    return convertir_usuario_a_respuesta(usuario_guardado), None


def actualizar_usuario_con_validaciones(id_usuario, datos):
    """Valida datos y actualiza un usuario existente en PostgreSQL.

    Si llega password, se cambia. Si no llega, se conserva el password actual.
    """
    usuario = consultar_usuario_por_id_en_bd(id_usuario)
    if not usuario:
        return None, {"usuario": "No existe un usuario con ese id."}

    errores = validar_datos_para_guardar_usuario(datos, es_creacion=False)
    if errores:
        return None, errores

    correo = datos["correo"].strip().lower()
    usuario_existente = consultar_usuario_por_correo_en_bd(correo)
    if usuario_existente and usuario_existente.id_usuario != usuario.id_usuario:
        return None, {"correo": "Ya existe otro usuario con ese correo."}

    rol = consultar_rol_por_id_en_bd(datos["id_rol"])
    if not rol:
        return None, {"id_rol": "El rol indicado no existe."}

    id_sucursal = datos.get("id_sucursal")
    if id_sucursal and not consultar_sucursal_por_id_en_bd(id_sucursal):
        return None, {"id_sucursal": "La sucursal indicada no existe."}

    usuario.id_rol = datos["id_rol"]
    usuario.id_sucursal = id_sucursal
    usuario.nombre = datos["nombre"].strip()
    usuario.correo = correo
    usuario.activo = datos.get("activo", usuario.activo)

    if datos.get("password"):
        usuario.password_hash = generar_hash_password(datos["password"])

    usuario_guardado = guardar_usuario_en_base_de_datos(usuario)
    return convertir_usuario_a_respuesta(usuario_guardado), None
