from flask import Blueprint, jsonify

from app.modules.inventario.tipo_movimiento_inventario.service import (
    listar_tipos_movimiento_inventario_para_respuesta,
)

tipos_movimiento_inventario_bp = Blueprint("tipos_movimiento_inventario", __name__)


@tipos_movimiento_inventario_bp.get("/listar_tipos_movimiento_inventario")
def listar_tipos_movimiento_inventario_endpoint():
    """Lista el catalogo de tipos de movimiento de inventario."""
    return jsonify({"data": listar_tipos_movimiento_inventario_para_respuesta()}), 200
