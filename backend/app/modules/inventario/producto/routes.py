from flask import Blueprint, jsonify, request

from app.modules.inventario.producto.service import (
    actualizar_producto_con_validaciones,
    crear_producto_con_validaciones,
    listar_productos_para_respuesta,
    obtener_producto_para_respuesta,
)

productos_bp = Blueprint("productos", __name__)


@productos_bp.get("/listar_productos")
def listar_productos_endpoint():
    """Lista todos los productos."""
    return jsonify({"data": listar_productos_para_respuesta()}), 200


@productos_bp.get("/obtener_producto/<int:id_producto>")
def obtener_producto_endpoint(id_producto):
    """Consulta un producto por id."""
    producto = obtener_producto_para_respuesta(id_producto)
    if not producto:
        return jsonify({"message": "Producto no encontrado."}), 404

    return jsonify({"data": producto}), 200


@productos_bp.post("/crear_producto")
def crear_producto_endpoint():
    """Crea un producto nuevo."""
    datos = request.get_json(silent=True) or {}
    producto, errores = crear_producto_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el producto.", "errors": errores}), 400

    return jsonify({"message": "Producto creado correctamente.", "data": producto}), 201


@productos_bp.put("/actualizar_producto/<int:id_producto>")
def actualizar_producto_endpoint(id_producto):
    """Actualiza un producto existente."""
    datos = request.get_json(silent=True) or {}
    producto, errores = actualizar_producto_con_validaciones(id_producto, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el producto.", "errors": errores}), 400

    return jsonify({"message": "Producto actualizado correctamente.", "data": producto}), 200
