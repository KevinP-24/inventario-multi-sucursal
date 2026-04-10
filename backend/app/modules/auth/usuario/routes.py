from flask import Blueprint, jsonify, request

from app.modules.auth.usuario.service import (
    actualizar_usuario_con_validaciones,
    crear_usuario_con_validaciones,
    listar_usuarios_para_respuesta,
    obtener_usuario_para_respuesta,
)

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.get("/listar_usuarios")
def listar_usuarios_endpoint():
    """Lista los usuarios registrados."""
    return jsonify({"data": listar_usuarios_para_respuesta()}), 200


@usuarios_bp.get("/obtener_usuario/<int:id_usuario>")
def obtener_usuario_endpoint(id_usuario):
    """Consulta un usuario por id."""
    usuario = obtener_usuario_para_respuesta(id_usuario)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado."}), 404

    return jsonify({"data": usuario}), 200


@usuarios_bp.post("/crear_usuario")
def crear_usuario_endpoint():
    """Crea un usuario nuevo."""
    datos = request.get_json(silent=True) or {}
    usuario, errores = crear_usuario_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el usuario.", "errors": errores}), 400

    return jsonify({"message": "Usuario creado correctamente.", "data": usuario}), 201


@usuarios_bp.put("/actualizar_usuario/<int:id_usuario>")
def actualizar_usuario_endpoint(id_usuario):
    """Actualiza un usuario existente."""
    datos = request.get_json(silent=True) or {}
    usuario, errores = actualizar_usuario_con_validaciones(id_usuario, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el usuario.", "errors": errores}), 400

    return jsonify({"message": "Usuario actualizado correctamente.", "data": usuario}), 200
