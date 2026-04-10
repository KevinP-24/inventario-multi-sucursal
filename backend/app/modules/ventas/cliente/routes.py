from flask import Blueprint, jsonify, request

from app.modules.ventas.cliente.service import (
    actualizar_cliente_con_validaciones,
    crear_cliente_con_validaciones,
    listar_clientes_para_respuesta,
    obtener_cliente_para_respuesta,
)

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.get("/listar_clientes")
def listar_clientes_endpoint():
    """Lista todos los clientes."""
    return jsonify({"data": listar_clientes_para_respuesta()}), 200


@clientes_bp.get("/obtener_cliente/<int:id_cliente>")
def obtener_cliente_endpoint(id_cliente):
    """Consulta un cliente por id."""
    cliente = obtener_cliente_para_respuesta(id_cliente)
    if not cliente:
        return jsonify({"message": "Cliente no encontrado."}), 404

    return jsonify({"data": cliente}), 200


@clientes_bp.post("/crear_cliente")
def crear_cliente_endpoint():
    """Crea un cliente nuevo."""
    datos = request.get_json(silent=True) or {}
    cliente, errores = crear_cliente_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el cliente.", "errors": errores}), 400

    return jsonify({"message": "Cliente creado correctamente.", "data": cliente}), 201


@clientes_bp.put("/actualizar_cliente/<int:id_cliente>")
def actualizar_cliente_endpoint(id_cliente):
    """Actualiza un cliente existente."""
    datos = request.get_json(silent=True) or {}
    cliente, errores = actualizar_cliente_con_validaciones(id_cliente, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el cliente.", "errors": errores}), 400

    return jsonify({"message": "Cliente actualizado correctamente.", "data": cliente}), 200
