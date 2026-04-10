from flask import Blueprint, jsonify, request

from app.modules.ventas.venta.service import (
    crear_venta_con_validaciones,
    listar_ventas_para_respuesta,
    obtener_venta_para_respuesta,
)

ventas_bp = Blueprint("ventas", __name__)


@ventas_bp.get("/listar_ventas")
def listar_ventas_endpoint():
    """Lista las ventas registradas."""
    return jsonify({"data": listar_ventas_para_respuesta()}), 200


@ventas_bp.get("/obtener_venta/<int:id_venta>")
def obtener_venta_endpoint(id_venta):
    """Consulta una venta por id."""
    venta = obtener_venta_para_respuesta(id_venta)
    if not venta:
        return jsonify({"message": "Venta no encontrada."}), 404

    return jsonify({"data": venta}), 200


@ventas_bp.post("/crear_venta")
def crear_venta_endpoint():
    """Registra una venta: valida stock, descuenta inventario y genera comprobante."""
    datos = request.get_json(silent=True) or {}
    venta, errores = crear_venta_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo registrar la venta.", "errors": errores}), 400

    return jsonify({"message": "Venta registrada correctamente.", "data": venta}), 201
