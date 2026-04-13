from flask import Blueprint, jsonify

from app.modules.transferencias.detalle_transferencia.service import (
    listar_detalles_por_transferencia_para_respuesta,
)

detalles_transferencia_bp = Blueprint("detalles_transferencia", __name__)


@detalles_transferencia_bp.get("/listar_detalles_por_transferencia/<int:id_transferencia>")
def listar_detalles_por_transferencia_endpoint(id_transferencia):
    """Lista los productos solicitados en una transferencia."""
    return jsonify({"data": listar_detalles_por_transferencia_para_respuesta(id_transferencia)}), 200
