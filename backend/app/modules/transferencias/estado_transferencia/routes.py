from flask import Blueprint, jsonify

from app.modules.transferencias.estado_transferencia.service import (
    listar_estados_transferencia_para_respuesta,
)

estados_transferencia_bp = Blueprint("estados_transferencia", __name__)


@estados_transferencia_bp.get("/listar_estados_transferencia")
def listar_estados_transferencia_endpoint():
    """Lista el catalogo de estados del ciclo de transferencias."""
    return jsonify({"data": listar_estados_transferencia_para_respuesta()}), 200
