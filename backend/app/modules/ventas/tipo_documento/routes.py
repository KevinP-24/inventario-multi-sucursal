from flask import Blueprint, jsonify

from app.modules.ventas.tipo_documento.service import listar_tipos_documento_para_respuesta

tipos_documento_bp = Blueprint("tipos_documento", __name__)


@tipos_documento_bp.get("/listar_tipos_documento")
def listar_tipos_documento_endpoint():
    """Lista los tipos de documento soportados para clientes."""
    return jsonify({"data": listar_tipos_documento_para_respuesta()}), 200
