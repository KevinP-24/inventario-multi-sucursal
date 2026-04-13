from flask import Blueprint, jsonify, request

from app.modules.inventario.precio_producto.service import (
    actualizar_precio_producto_con_validaciones,
    crear_precio_producto_con_validaciones,
    listar_precios_producto_para_respuesta,
    obtener_precio_producto_para_respuesta,
)

precios_producto_bp = Blueprint("precios_producto", __name__)


@precios_producto_bp.get("/listar_precios_producto")
def listar_precios_producto_endpoint():
    """Lista todos los precios de producto."""
    return jsonify({"data": listar_precios_producto_para_respuesta()}), 200


@precios_producto_bp.get("/obtener_precio_producto/<int:id_precio_producto>")
def obtener_precio_producto_endpoint(id_precio_producto):
    """Consulta un precio de producto por id."""
    precio = obtener_precio_producto_para_respuesta(id_precio_producto)
    if not precio:
        return jsonify({"message": "Precio de producto no encontrado."}), 404

    return jsonify({"data": precio}), 200


@precios_producto_bp.post("/crear_precio_producto")
def crear_precio_producto_endpoint():
    """Crea un precio para un producto en una lista."""
    datos = request.get_json(silent=True) or {}
    precio, errores = crear_precio_producto_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el precio.", "errors": errores}), 400

    return jsonify({"message": "Precio creado correctamente.", "data": precio}), 201


@precios_producto_bp.put("/actualizar_precio_producto/<int:id_precio_producto>")
def actualizar_precio_producto_endpoint(id_precio_producto):
    """Actualiza un precio de producto existente."""
    datos = request.get_json(silent=True) or {}
    precio, errores = actualizar_precio_producto_con_validaciones(id_precio_producto, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el precio.", "errors": errores}), 400

    return jsonify({"message": "Precio actualizado correctamente.", "data": precio}), 200
