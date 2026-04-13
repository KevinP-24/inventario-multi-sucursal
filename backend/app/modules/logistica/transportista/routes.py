from flask import Blueprint, jsonify, request

from app.modules.logistica.transportista.service import (
    actualizar_transportista_con_validaciones,
    crear_transportista_con_validaciones,
    listar_transportistas_para_respuesta,
    obtener_transportista_para_respuesta,
)

transportistas_bp = Blueprint("transportistas", __name__)


@transportistas_bp.get("/listar_transportistas")
def listar_transportistas_endpoint():
    """Lista todos los transportistas."""
    return jsonify({"data": listar_transportistas_para_respuesta()}), 200


@transportistas_bp.get("/obtener_transportista/<int:id_transportista>")
def obtener_transportista_endpoint(id_transportista):
    """Consulta un transportista por id."""
    transportista = obtener_transportista_para_respuesta(id_transportista)
    if not transportista:
        return jsonify({"message": "Transportista no encontrado."}), 404

    return jsonify({"data": transportista}), 200


@transportistas_bp.post("/crear_transportista")
def crear_transportista_endpoint():
    """Crea un transportista nuevo."""
    datos = request.get_json(silent=True) or {}
    transportista, errores = crear_transportista_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el transportista.", "errors": errores}), 400

    return jsonify({"message": "Transportista creado correctamente.", "data": transportista}), 201


@transportistas_bp.put("/actualizar_transportista/<int:id_transportista>")
def actualizar_transportista_endpoint(id_transportista):
    """Actualiza un transportista existente."""
    datos = request.get_json(silent=True) or {}
    transportista, errores = actualizar_transportista_con_validaciones(id_transportista, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el transportista.", "errors": errores}), 400

    return jsonify({"message": "Transportista actualizado correctamente.", "data": transportista}), 200
