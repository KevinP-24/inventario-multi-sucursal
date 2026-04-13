from flask import Blueprint, jsonify, request

from app.modules.compras.orden_compra.service import (
    anular_orden_compra_con_validaciones,
    crear_orden_compra_con_validaciones,
    filtrar_historial_compras_para_respuesta,
    listar_ordenes_compra_para_respuesta,
    obtener_orden_compra_para_respuesta,
    recibir_orden_compra_con_validaciones,
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


@ordenes_compra_bp.get("/filtrar_historial_compras")
def filtrar_historial_compras_endpoint():
    """Consulta historico de compras por proveedor, producto, sucursal, estado o fechas."""
    ordenes, errores = filtrar_historial_compras_para_respuesta(request.args)

    if errores:
        return jsonify({"message": "No se pudo filtrar el historico de compras.", "errors": errores}), 400

    return jsonify({"data": ordenes}), 200


@ordenes_compra_bp.post("/crear_orden_compra")
def crear_orden_compra_endpoint():
    """Crea una orden de compra con sus detalles."""
    datos = request.get_json(silent=True) or {}
    orden, errores = crear_orden_compra_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la orden de compra.", "errors": errores}), 400

    return jsonify({"message": "Orden de compra creada correctamente.", "data": orden}), 201


@ordenes_compra_bp.post("/anular_orden_compra/<int:id_orden_compra>")
def anular_orden_compra_endpoint(id_orden_compra):
    """Anula una orden de compra registrada antes de su recepcion."""
    orden, errores = anular_orden_compra_con_validaciones(id_orden_compra)

    if errores:
        codigo_estado = 404 if "orden_compra" in errores else 400
        return jsonify({
            "message": "No se pudo anular la orden de compra.",
            "errors": errores,
        }), codigo_estado

    return jsonify({"message": "Orden de compra anulada correctamente.", "data": orden}), 200


@ordenes_compra_bp.post("/recibir_orden_compra/<int:id_orden_compra>")
def recibir_orden_compra_endpoint(id_orden_compra):
    """Recibe una orden de compra y suma sus productos al inventario."""
    datos = request.get_json(silent=True) or {}
    orden, movimientos, errores = recibir_orden_compra_con_validaciones(id_orden_compra, datos)

    if errores:
        codigo_estado = 404 if "orden_compra" in errores else 400
        return jsonify({
            "message": "No se pudo recibir la orden de compra.",
            "errors": errores,
        }), codigo_estado

    return jsonify({
        "message": "Orden de compra recibida correctamente.",
        "data": {
            "orden_compra": orden,
            "movimientos_inventario": movimientos,
        },
    }), 200
