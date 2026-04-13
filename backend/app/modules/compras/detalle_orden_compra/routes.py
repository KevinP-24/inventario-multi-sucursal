from flask import Blueprint, jsonify

from app.modules.compras.detalle_orden_compra.service import (
    listar_detalles_por_orden_compra_para_respuesta,
)

detalles_orden_compra_bp = Blueprint("detalles_orden_compra", __name__)


@detalles_orden_compra_bp.get("/listar_detalles_por_orden_compra/<int:id_orden_compra>")
def listar_detalles_por_orden_compra_endpoint(id_orden_compra):
    """Lista los detalles asociados a una orden de compra."""
    detalles = listar_detalles_por_orden_compra_para_respuesta(id_orden_compra)
    return jsonify({"data": detalles}), 200
