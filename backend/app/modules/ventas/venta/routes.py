from datetime import datetime, time

from flask import Blueprint, jsonify, request

from app.modules.ventas.venta.service import (
    crear_venta_con_validaciones,
    listar_ventas_para_respuesta,
    obtener_venta_para_respuesta,
)

ventas_bp = Blueprint("ventas", __name__)


@ventas_bp.get("/listar_ventas")
def listar_ventas_endpoint():
    """Lista las ventas registradas con filtros opcionales."""
    filtros = {
        "id_sucursal": request.args.get("id_sucursal", type=int),
        "id_cliente": request.args.get("id_cliente", type=int),
    }

    fecha_inicio_str = request.args.get("fecha_inicio")
    fecha_fin_str = request.args.get("fecha_fin")

    if fecha_inicio_str:
        try:
            filtros["fecha_inicio"] = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "Formato de fecha_inicio invalido. Use YYYY-MM-DD."}), 400

    if fecha_fin_str:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            filtros["fecha_fin"] = datetime.combine(fecha_fin_dt, time.max)
        except ValueError:
            return jsonify({"message": "Formato de fecha_fin invalido. Use YYYY-MM-DD."}), 400

    return jsonify({"data": listar_ventas_para_respuesta(filtros)}), 200


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
