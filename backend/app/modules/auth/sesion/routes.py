from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.modules.auth.sesion.service import iniciar_sesion_con_validaciones
from app.modules.auth.usuario.service import obtener_usuario_para_respuesta

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login_endpoint():
    """Autentica usuario y retorna token JWT."""
    datos = request.get_json(silent=True) or {}
    token, usuario, errores = iniciar_sesion_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo iniciar sesion.", "errors": errores}), 401

    return jsonify({
        "message": "Sesion iniciada correctamente.",
        "access_token": token,
        "token_type": "Bearer",
        "usuario": usuario,
    }), 200


@auth_bp.get("/me")
@jwt_required()
def me_endpoint():
    """Devuelve el usuario autenticado."""
    usuario = obtener_usuario_para_respuesta(int(get_jwt_identity()))
    if not usuario:
        return jsonify({"message": "Usuario no encontrado."}), 404

    return jsonify({"data": usuario}), 200
