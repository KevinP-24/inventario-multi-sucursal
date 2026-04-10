from flask import Blueprint, jsonify, request

from app.modules.compras.orden_compra.service import (
    crear_orden_compra_con_validaciones,
    listar_ordenes_compra_para_respuesta,
    obtener_orden_compra_para_respuesta,
)

ordenes_compra_bp = Blueprint("ordenes_compra", __name__)


@ordenes_compra_bp.get("/listar_ordenes_compra")
def listar_ordenes_compra_endpoint():
    """Lista todas las ordenes de compra."""
    return jsonify({"data": listar_ordenes_compra_para_respuesta()}), 200


@ordenes_compra_bp.get("/obtener_orden_compra/<int:id_orden_compra>")
def obtener_orden_compra_endpoint(id_orden_compra):
    """Consulta una orden de compra por id."""
    orden = obtener_orden_compra_para_respuesta(id_orden_compra)
    if not orden:
        return jsonify({"message": "Orden de compra no encontrada."}), 404

    return jsonify({"data": orden}), 200


@ordenes_compra_bp.post("/crear_orden_compra")
def crear_orden_compra_endpoint():
    """Crea una orden de compra con sus detalles."""
    datos = request.get_json(silent=True) or {}
    orden, errores = crear_orden_compra_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la orden de compra.", "errors": errores}), 400

    return jsonify({"message": "Orden de compra creada correctamente.", "data": orden}), 201
