from flask import Blueprint, jsonify, request

from app.modules.sucursales.sucursal.service import (
    actualizar_sucursal_con_validaciones,
    crear_sucursal_con_validaciones,
    listar_sucursales_para_respuesta,
    obtener_sucursal_para_respuesta,
)

sucursales_bp = Blueprint("sucursales", __name__)


@sucursales_bp.get("/listar_sucursales")
def listar_sucursales_endpoint():
    """Lista todas las sucursales registradas."""
    return jsonify({"data": listar_sucursales_para_respuesta()}), 200


@sucursales_bp.get("/obtener_sucursal/<int:id_sucursal>")
def obtener_sucursal_endpoint(id_sucursal):
    """Consulta una sucursal por id."""
    sucursal = obtener_sucursal_para_respuesta(id_sucursal)
    if not sucursal:
        return jsonify({"message": "Sucursal no encontrada."}), 404

    return jsonify({"data": sucursal}), 200


@sucursales_bp.post("/crear_sucursal")
def crear_sucursal_endpoint():
    """Crea una sucursal nueva."""
    datos = request.get_json(silent=True) or {}
    sucursal, errores = crear_sucursal_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la sucursal.", "errors": errores}), 400

    return jsonify({"message": "Sucursal creada correctamente.", "data": sucursal}), 201


@sucursales_bp.put("/actualizar_sucursal/<int:id_sucursal>")
def actualizar_sucursal_endpoint(id_sucursal):
    """Actualiza una sucursal existente."""
    datos = request.get_json(silent=True) or {}
    sucursal, errores = actualizar_sucursal_con_validaciones(id_sucursal, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar la sucursal.", "errors": errores}), 400

    return jsonify({"message": "Sucursal actualizada correctamente.", "data": sucursal}), 200
