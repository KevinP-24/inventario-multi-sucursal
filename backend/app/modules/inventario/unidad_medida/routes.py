from flask import Blueprint, jsonify, request

from app.modules.inventario.unidad_medida.service import (
    actualizar_unidad_medida_con_validaciones,
    crear_unidad_medida_con_validaciones,
    listar_unidades_medida_para_respuesta,
    obtener_unidad_medida_para_respuesta,
)

unidades_medida_bp = Blueprint("unidades_medida", __name__)


@unidades_medida_bp.get("/listar_unidades_medida")
def listar_unidades_medida_endpoint():
    """Lista todas las unidades de medida."""
    return jsonify({"data": listar_unidades_medida_para_respuesta()}), 200


@unidades_medida_bp.get("/obtener_unidad_medida/<int:id_unidad>")
def obtener_unidad_medida_endpoint(id_unidad):
    """Consulta una unidad de medida por id."""
    unidad = obtener_unidad_medida_para_respuesta(id_unidad)
    if not unidad:
        return jsonify({"message": "Unidad de medida no encontrada."}), 404

    return jsonify({"data": unidad}), 200


@unidades_medida_bp.post("/crear_unidad_medida")
def crear_unidad_medida_endpoint():
    """Crea una unidad de medida nueva."""
    datos = request.get_json(silent=True) or {}
    unidad, errores = crear_unidad_medida_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la unidad de medida.", "errors": errores}), 400

    return jsonify({"message": "Unidad de medida creada correctamente.", "data": unidad}), 201


@unidades_medida_bp.put("/actualizar_unidad_medida/<int:id_unidad>")
def actualizar_unidad_medida_endpoint(id_unidad):
    """Actualiza una unidad de medida existente."""
    datos = request.get_json(silent=True) or {}
    unidad, errores = actualizar_unidad_medida_con_validaciones(id_unidad, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar la unidad de medida.", "errors": errores}), 400

    return jsonify({"message": "Unidad de medida actualizada correctamente.", "data": unidad}), 200
