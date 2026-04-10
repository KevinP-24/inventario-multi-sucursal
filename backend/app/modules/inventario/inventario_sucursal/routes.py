from flask import Blueprint, jsonify, request

from app.modules.inventario.inventario_sucursal.service import (
    actualizar_inventario_sucursal_con_validaciones,
    crear_inventario_sucursal_con_validaciones,
    listar_inventario_sucursal_para_respuesta,
    obtener_inventario_sucursal_para_respuesta,
)

inventario_sucursal_bp = Blueprint("inventario_sucursal", __name__)


@inventario_sucursal_bp.get("/listar_inventario_sucursal")
def listar_inventario_sucursal_endpoint():
    """Lista el stock actual por sucursal y producto."""
    return jsonify({"data": listar_inventario_sucursal_para_respuesta()}), 200


@inventario_sucursal_bp.get("/obtener_inventario_sucursal/<int:id_inventario>")
def obtener_inventario_sucursal_endpoint(id_inventario):
    """Consulta un registro de inventario por id."""
    inventario = obtener_inventario_sucursal_para_respuesta(id_inventario)
    if not inventario:
        return jsonify({"message": "Inventario de sucursal no encontrado."}), 404

    return jsonify({"data": inventario}), 200


@inventario_sucursal_bp.post("/crear_inventario_sucursal")
def crear_inventario_sucursal_endpoint():
    """Crea el stock inicial de un producto en una sucursal."""
    datos = request.get_json(silent=True) or {}
    inventario, errores = crear_inventario_sucursal_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el inventario.", "errors": errores}), 400

    return jsonify({"message": "Inventario creado correctamente.", "data": inventario}), 201


@inventario_sucursal_bp.put("/actualizar_inventario_sucursal/<int:id_inventario>")
def actualizar_inventario_sucursal_endpoint(id_inventario):
    """Actualiza cantidad actual y costo promedio."""
    datos = request.get_json(silent=True) or {}
    inventario, errores = actualizar_inventario_sucursal_con_validaciones(id_inventario, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el inventario.", "errors": errores}), 400

    return jsonify({"message": "Inventario actualizado correctamente.", "data": inventario}), 200
