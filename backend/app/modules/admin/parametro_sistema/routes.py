from flask import Blueprint, jsonify, request

from app.modules.admin.parametro_sistema.service import (
    actualizar_parametro_sistema_con_validaciones,
    crear_parametro_sistema_con_validaciones,
    listar_parametros_sistema_para_respuesta,
    obtener_parametro_sistema_para_respuesta,
)

parametros_sistema_bp = Blueprint("parametros_sistema", __name__)


@parametros_sistema_bp.get("/listar_parametros_sistema")
def listar_parametros_sistema_endpoint():
    """Lista todos los parametros del sistema."""
    return jsonify({"data": listar_parametros_sistema_para_respuesta()}), 200


@parametros_sistema_bp.get("/obtener_parametro_sistema/<int:id_parametro>")
def obtener_parametro_sistema_endpoint(id_parametro):
    """Consulta un parametro del sistema por id."""
    parametro = obtener_parametro_sistema_para_respuesta(id_parametro)
    if not parametro:
        return jsonify({"message": "Parametro no encontrado."}), 404

    return jsonify({"data": parametro}), 200


@parametros_sistema_bp.post("/crear_parametro_sistema")
def crear_parametro_sistema_endpoint():
    """Crea un parametro del sistema nuevo."""
    datos = request.get_json(silent=True) or {}
    parametro, errores = crear_parametro_sistema_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el parametro.", "errors": errores}), 400

    return jsonify({"message": "Parametro creado correctamente.", "data": parametro}), 201


@parametros_sistema_bp.put("/actualizar_parametro_sistema/<int:id_parametro>")
def actualizar_parametro_sistema_endpoint(id_parametro):
    """Actualiza un parametro del sistema existente."""
    datos = request.get_json(silent=True) or {}
    parametro, errores = actualizar_parametro_sistema_con_validaciones(id_parametro, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el parametro.", "errors": errores}), 400

    return jsonify({"message": "Parametro actualizado correctamente.", "data": parametro}), 200
