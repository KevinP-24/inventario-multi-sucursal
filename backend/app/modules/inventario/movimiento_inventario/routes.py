from flask import Blueprint, jsonify, request

from app.modules.inventario.movimiento_inventario.service import (
    listar_movimientos_inventario_para_respuesta,
    listar_movimientos_por_inventario_para_respuesta,
    obtener_movimiento_inventario_para_respuesta,
    registrar_movimiento_inventario_con_validaciones,
)

movimientos_inventario_bp = Blueprint("movimientos_inventario", __name__)


@movimientos_inventario_bp.get("/listar_movimientos_inventario")
def listar_movimientos_inventario_endpoint():
    """Lista todo el historial de inventario."""
    return jsonify({"data": listar_movimientos_inventario_para_respuesta()}), 200


@movimientos_inventario_bp.get("/obtener_movimiento_inventario/<int:id_movimiento>")
def obtener_movimiento_inventario_endpoint(id_movimiento):
    """Consulta un movimiento de inventario por id."""
    movimiento = obtener_movimiento_inventario_para_respuesta(id_movimiento)
    if not movimiento:
        return jsonify({"message": "Movimiento de inventario no encontrado."}), 404

    return jsonify({"data": movimiento}), 200


@movimientos_inventario_bp.get("/listar_movimientos_por_inventario/<int:id_inventario>")
def listar_movimientos_por_inventario_endpoint(id_inventario):
    """Lista el historial de un inventario especifico."""
    return jsonify({"data": listar_movimientos_por_inventario_para_respuesta(id_inventario)}), 200


@movimientos_inventario_bp.post("/registrar_movimiento_inventario")
def registrar_movimiento_inventario_endpoint():
    """Registra trazabilidad de un cambio de inventario."""
    datos = request.get_json(silent=True) or {}
    movimiento, errores = registrar_movimiento_inventario_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo registrar el movimiento.", "errors": errores}), 400

    return jsonify({"message": "Movimiento registrado correctamente.", "data": movimiento}), 201
