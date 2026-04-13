from flask_jwt_extended import create_access_token

from app.modules.auth.usuario.repository import consultar_usuario_por_correo_en_bd
from app.modules.auth.usuario.schema import convertir_usuario_a_respuesta
from app.security.password import verificar_password
from app.modules.auth.sesion.schema import validar_datos_login


def iniciar_sesion_con_validaciones(datos):
    """Valida credenciales y emite un access token JWT."""
    errores = validar_datos_login(datos)
    if errores:
        return None, None, errores

    correo = datos["correo"].strip().lower()
    usuario = consultar_usuario_por_correo_en_bd(correo)
    if not usuario or not verificar_password(datos["password"], usuario.password_hash):
        return None, None, {"credenciales": "Correo o contrasena incorrectos."}

    if not usuario.activo:
        return None, None, {"usuario": "El usuario se encuentra inactivo."}

    if not usuario.rol or not usuario.rol.activo:
        return None, None, {"rol": "El rol del usuario no esta activo."}

    claims = {
        "id_usuario": usuario.id_usuario,
        "correo": usuario.correo,
        "rol": usuario.rol.nombre,
        "id_rol": usuario.id_rol,
        "id_sucursal": usuario.id_sucursal,
    }
    token = create_access_token(identity=str(usuario.id_usuario), additional_claims=claims)

    return token, convertir_usuario_a_respuesta(usuario), None
