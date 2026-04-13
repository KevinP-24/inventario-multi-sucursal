from flask import Blueprint, jsonify, request

from app.modules.inventario.lista_precio.service import (
    actualizar_lista_precio_con_validaciones,
    crear_lista_precio_con_validaciones,
    listar_listas_precio_para_respuesta,
    obtener_lista_precio_para_respuesta,
)

listas_precio_bp = Blueprint("listas_precio", __name__)


@listas_precio_bp.get("/listar_listas_precio")
def listar_listas_precio_endpoint():
    """Lista todas las listas de precio."""
    return jsonify({"data": listar_listas_precio_para_respuesta()}), 200


@listas_precio_bp.get("/obtener_lista_precio/<int:id_lista_precio>")
def obtener_lista_precio_endpoint(id_lista_precio):
    """Consulta una lista de precio por id."""
    lista = obtener_lista_precio_para_respuesta(id_lista_precio)
    if not lista:
        return jsonify({"message": "Lista de precio no encontrada."}), 404

    return jsonify({"data": lista}), 200


@listas_precio_bp.post("/crear_lista_precio")
def crear_lista_precio_endpoint():
    """Crea una lista de precio nueva."""
    datos = request.get_json(silent=True) or {}
    lista, errores = crear_lista_precio_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la lista de precio.", "errors": errores}), 400

    return jsonify({"message": "Lista de precio creada correctamente.", "data": lista}), 201


@listas_precio_bp.put("/actualizar_lista_precio/<int:id_lista_precio>")
def actualizar_lista_precio_endpoint(id_lista_precio):
    """Actualiza una lista de precio existente."""
    datos = request.get_json(silent=True) or {}
    lista, errores = actualizar_lista_precio_con_validaciones(id_lista_precio, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar la lista de precio.", "errors": errores}), 400

    return jsonify({"message": "Lista de precio actualizada correctamente.", "data": lista}), 200
