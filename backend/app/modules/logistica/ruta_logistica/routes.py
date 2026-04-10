from flask import Blueprint, jsonify, request

from app.modules.logistica.ruta_logistica.service import (
    actualizar_ruta_logistica_con_validaciones,
    crear_ruta_logistica_con_validaciones,
    listar_rutas_logistica_para_respuesta,
    obtener_ruta_logistica_para_respuesta,
)

rutas_logistica_bp = Blueprint("rutas_logistica", __name__)


@rutas_logistica_bp.get("/listar_rutas_logistica")
def listar_rutas_logistica_endpoint():
    """Lista todas las rutas logisticas."""
    return jsonify({"data": listar_rutas_logistica_para_respuesta()}), 200


@rutas_logistica_bp.get("/obtener_ruta_logistica/<int:id_ruta>")
def obtener_ruta_logistica_endpoint(id_ruta):
    """Consulta una ruta logistica por id."""
    ruta = obtener_ruta_logistica_para_respuesta(id_ruta)
    if not ruta:
        return jsonify({"message": "Ruta logistica no encontrada."}), 404

    return jsonify({"data": ruta}), 200


@rutas_logistica_bp.post("/crear_ruta_logistica")
def crear_ruta_logistica_endpoint():
    """Crea una ruta logistica nueva."""
    datos = request.get_json(silent=True) or {}
    ruta, errores = crear_ruta_logistica_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la ruta logistica.", "errors": errores}), 400

    return jsonify({"message": "Ruta logistica creada correctamente.", "data": ruta}), 201


@rutas_logistica_bp.put("/actualizar_ruta_logistica/<int:id_ruta>")
def actualizar_ruta_logistica_endpoint(id_ruta):
    """Actualiza una ruta logistica existente."""
    datos = request.get_json(silent=True) or {}
    ruta, errores = actualizar_ruta_logistica_con_validaciones(id_ruta, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar la ruta logistica.", "errors": errores}), 400

    return jsonify({"message": "Ruta logistica actualizada correctamente.", "data": ruta}), 200
