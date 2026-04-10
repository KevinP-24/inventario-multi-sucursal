from flask import Blueprint, jsonify

from app.modules.logistica.prioridad_ruta_logistica.service import (
    listar_prioridades_ruta_logistica_para_respuesta,
)

prioridades_ruta_logistica_bp = Blueprint("prioridades_ruta_logistica", __name__)


@prioridades_ruta_logistica_bp.get("/listar_prioridades_ruta_logistica")
def listar_prioridades_ruta_logistica_endpoint():
    """Lista el catalogo de prioridades de rutas logisticas."""
    return jsonify({"data": listar_prioridades_ruta_logistica_para_respuesta()}), 200
