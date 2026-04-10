from flask import Blueprint, jsonify, request

from app.modules.dashboard.service import (
    comparar_rendimiento_sucursales_para_respuesta,
    consultar_indicadores_reabastecimiento_para_respuesta,
    consultar_rotacion_y_demanda_para_respuesta,
    consultar_transferencias_activas_para_respuesta,
    consultar_volumen_ventas_para_respuesta,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/volumen_ventas")
def volumen_ventas_endpoint():
    """Compara ventas del mes en curso contra periodos anteriores."""
    id_sucursal = request.args.get("id_sucursal", type=int)
    meses = request.args.get("meses", default=6, type=int)
    return jsonify({"data": consultar_volumen_ventas_para_respuesta(id_sucursal, meses)}), 200


@dashboard_bp.get("/rotacion_demanda")
def rotacion_demanda_endpoint():
    """Consulta rotacion de inventario y productos de alta o baja demanda."""
    id_sucursal = request.args.get("id_sucursal", type=int)
    limite = request.args.get("limite", default=10, type=int)
    return jsonify({"data": consultar_rotacion_y_demanda_para_respuesta(id_sucursal, limite)}), 200


@dashboard_bp.get("/transferencias_activas")
def transferencias_activas_endpoint():
    """Visualiza transferencias activas y su impacto en inventario."""
    id_sucursal = request.args.get("id_sucursal", type=int)
    return jsonify({"data": consultar_transferencias_activas_para_respuesta(id_sucursal)}), 200


@dashboard_bp.get("/reabastecimiento")
def reabastecimiento_endpoint():
    """Consulta productos bajo minimo o proximos a agotarse."""
    id_sucursal = request.args.get("id_sucursal", type=int)
    return jsonify({"data": consultar_indicadores_reabastecimiento_para_respuesta(id_sucursal)}), 200


@dashboard_bp.get("/rendimiento_sucursales")
def rendimiento_sucursales_endpoint():
    """Compara indicadores operativos entre sucursales."""
    return jsonify({"data": comparar_rendimiento_sucursales_para_respuesta()}), 200
