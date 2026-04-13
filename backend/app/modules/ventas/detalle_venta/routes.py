from flask import Blueprint, jsonify

from app.modules.ventas.detalle_venta.service import listar_detalles_por_venta_para_respuesta

detalles_venta_bp = Blueprint("detalles_venta", __name__)


@detalles_venta_bp.get("/listar_detalles_por_venta/<int:id_venta>")
def listar_detalles_por_venta_endpoint(id_venta):
    """Lista los productos incluidos en una venta."""
    return jsonify({"data": listar_detalles_por_venta_para_respuesta(id_venta)}), 200
