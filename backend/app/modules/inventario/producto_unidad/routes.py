from flask import Blueprint, jsonify, request

from app.modules.inventario.producto_unidad.service import (
    actualizar_producto_unidad_con_validaciones,
    crear_producto_unidad_con_validaciones,
    dar_baja_producto_unidad_con_validaciones,
    listar_producto_unidades_para_respuesta,
    obtener_producto_unidad_para_respuesta,
)

producto_unidades_bp = Blueprint("producto_unidades", __name__)


@producto_unidades_bp.get("/listar_producto_unidades")
def listar_producto_unidades_endpoint():
    """Lista todas las conversiones producto-unidad."""
    return jsonify({"data": listar_producto_unidades_para_respuesta()}), 200


@producto_unidades_bp.get("/obtener_producto_unidad/<int:id_producto_unidad>")
def obtener_producto_unidad_endpoint(id_producto_unidad):
    """Consulta una conversion producto-unidad por id."""
    conversion = obtener_producto_unidad_para_respuesta(id_producto_unidad)
    if not conversion:
        return jsonify({"message": "Conversion producto-unidad no encontrada."}), 404

    return jsonify({"data": conversion}), 200


@producto_unidades_bp.post("/crear_producto_unidad")
def crear_producto_unidad_endpoint():
    """Crea una conversion producto-unidad nueva."""
    datos = request.get_json(silent=True) or {}
    conversion, errores = crear_producto_unidad_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la conversion.", "errors": errores}), 400

    return jsonify({"message": "Conversion creada correctamente.", "data": conversion}), 201


@producto_unidades_bp.put("/actualizar_producto_unidad/<int:id_producto_unidad>")
def actualizar_producto_unidad_endpoint(id_producto_unidad):
    """Actualiza una conversion producto-unidad existente."""
    datos = request.get_json(silent=True) or {}
    conversion, errores = actualizar_producto_unidad_con_validaciones(id_producto_unidad, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar la conversion.", "errors": errores}), 400

    return jsonify({"message": "Conversion actualizada correctamente.", "data": conversion}), 200


@producto_unidades_bp.delete("/eliminar_producto_unidad/<int:id_producto_unidad>")
def eliminar_producto_unidad_endpoint(id_producto_unidad):
    """Da de baja una conversion producto-unidad sin eliminar su trazabilidad."""
    conversion, errores = dar_baja_producto_unidad_con_validaciones(id_producto_unidad)

    if errores:
        return jsonify({"message": "No se pudo dar de baja la conversion.", "errors": errores}), 400

    return jsonify({"message": "Conversion dada de baja correctamente.", "data": conversion}), 200
