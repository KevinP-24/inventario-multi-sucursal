from flask import Blueprint, jsonify, request

from app.modules.inventario.inventario_sucursal.service import (
    actualizar_inventario_sucursal_con_validaciones,
    ajustar_inventario_sucursal_con_validaciones,
    crear_inventario_sucursal_con_validaciones,
    listar_alertas_stock_bajo_para_respuesta,
    listar_inventario_sucursal_para_respuesta,
    obtener_inventario_sucursal_para_respuesta,
    registrar_devolucion_inventario_con_validaciones,
    registrar_merma_inventario_con_validaciones,
)

inventario_sucursal_bp = Blueprint("inventario_sucursal", __name__)


@inventario_sucursal_bp.get("/listar_inventario_sucursal")
def listar_inventario_sucursal_endpoint():
    """Lista el stock actual por sucursal y producto."""
    return jsonify({"data": listar_inventario_sucursal_para_respuesta()}), 200


@inventario_sucursal_bp.get("/listar_alertas_stock_bajo")
def listar_alertas_stock_bajo_endpoint():
    """Lista productos que estan en o por debajo del stock minimo."""
    id_sucursal = request.args.get("id_sucursal", type=int)
    alertas = listar_alertas_stock_bajo_para_respuesta(id_sucursal)
    return jsonify({"data": alertas}), 200


@inventario_sucursal_bp.get("/obtener_inventario_sucursal/<int:id_inventario>")
def obtener_inventario_sucursal_endpoint(id_inventario):
    """Consulta un registro de inventario por id."""
    inventario = obtener_inventario_sucursal_para_respuesta(id_inventario)
    if not inventario:
        return jsonify({"message": "Inventario de sucursal no encontrado."}), 404

    return jsonify({"data": inventario}), 200


@inventario_sucursal_bp.post("/crear_inventario_sucursal")
def crear_inventario_sucursal_endpoint():
    """Crea el stock inicial de un producto en una sucursal."""
    datos = request.get_json(silent=True) or {}
    inventario, errores = crear_inventario_sucursal_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el inventario.", "errors": errores}), 400

    return jsonify({"message": "Inventario creado correctamente.", "data": inventario}), 201


@inventario_sucursal_bp.put("/actualizar_inventario_sucursal/<int:id_inventario>")
def actualizar_inventario_sucursal_endpoint(id_inventario):
    """Actualiza cantidad actual y costo promedio."""
    datos = request.get_json(silent=True) or {}
    inventario, errores = actualizar_inventario_sucursal_con_validaciones(id_inventario, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el inventario.", "errors": errores}), 400

    return jsonify({"message": "Inventario actualizado correctamente.", "data": inventario}), 200


@inventario_sucursal_bp.post("/ajustar_inventario_sucursal/<int:id_inventario>")
def ajustar_inventario_sucursal_endpoint(id_inventario):
    """Registra una entrada, salida o ajuste manual con trazabilidad."""
    datos = request.get_json(silent=True) or {}
    inventario, movimiento, errores = ajustar_inventario_sucursal_con_validaciones(
        id_inventario,
        datos,
    )

    if errores:
        return jsonify({"message": "No se pudo ajustar el inventario.", "errors": errores}), 400

    return jsonify({
        "message": "Inventario ajustado correctamente.",
        "data": {
            "inventario": inventario,
            "movimiento": movimiento,
        },
    }), 200


@inventario_sucursal_bp.post("/registrar_devolucion_inventario/<int:id_inventario>")
def registrar_devolucion_inventario_endpoint(id_inventario):
    """Registra una devolucion y suma el producto al inventario disponible."""
    datos = request.get_json(silent=True) or {}
    inventario, movimiento, errores = registrar_devolucion_inventario_con_validaciones(
        id_inventario,
        datos,
    )

    if errores:
        return jsonify({"message": "No se pudo registrar la devolucion.", "errors": errores}), 400

    return jsonify({
        "message": "Devolucion registrada correctamente.",
        "data": {
            "inventario": inventario,
            "movimiento": movimiento,
        },
    }), 200


@inventario_sucursal_bp.post("/registrar_merma_inventario/<int:id_inventario>")
def registrar_merma_inventario_endpoint(id_inventario):
    """Registra una merma y descuenta el producto del inventario disponible."""
    datos = request.get_json(silent=True) or {}
    inventario, movimiento, errores = registrar_merma_inventario_con_validaciones(
        id_inventario,
        datos,
    )

    if errores:
        return jsonify({"message": "No se pudo registrar la merma.", "errors": errores}), 400

    return jsonify({
        "message": "Merma registrada correctamente.",
        "data": {
            "inventario": inventario,
            "movimiento": movimiento,
        },
    }), 200
