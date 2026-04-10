from flask import Blueprint, jsonify, request

from app.modules.compras.proveedor.service import (
    actualizar_proveedor_con_validaciones,
    crear_proveedor_con_validaciones,
    listar_proveedores_para_respuesta,
    obtener_proveedor_para_respuesta,
)

proveedores_bp = Blueprint("proveedores", __name__)


@proveedores_bp.get("/listar_proveedores")
def listar_proveedores_endpoint():
    """Lista todos los proveedores."""
    return jsonify({"data": listar_proveedores_para_respuesta()}), 200


@proveedores_bp.get("/obtener_proveedor/<int:id_proveedor>")
def obtener_proveedor_endpoint(id_proveedor):
    """Consulta un proveedor por id."""
    proveedor = obtener_proveedor_para_respuesta(id_proveedor)
    if not proveedor:
        return jsonify({"message": "Proveedor no encontrado."}), 404

    return jsonify({"data": proveedor}), 200


@proveedores_bp.post("/crear_proveedor")
def crear_proveedor_endpoint():
    """Crea un proveedor nuevo."""
    datos = request.get_json(silent=True) or {}
    proveedor, errores = crear_proveedor_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el proveedor.", "errors": errores}), 400

    return jsonify({"message": "Proveedor creado correctamente.", "data": proveedor}), 201


@proveedores_bp.put("/actualizar_proveedor/<int:id_proveedor>")
def actualizar_proveedor_endpoint(id_proveedor):
    """Actualiza un proveedor existente."""
    datos = request.get_json(silent=True) or {}
    proveedor, errores = actualizar_proveedor_con_validaciones(id_proveedor, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el proveedor.", "errors": errores}), 400

    return jsonify({"message": "Proveedor actualizado correctamente.", "data": proveedor}), 200
