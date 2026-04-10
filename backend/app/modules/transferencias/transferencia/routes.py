from flask import Blueprint, jsonify, request

from app.modules.transferencias.transferencia.service import (
    confirmar_recepcion_transferencia_con_validaciones,
    crear_transferencia_con_validaciones,
    listar_transferencias_para_respuesta,
    obtener_transferencia_para_respuesta,
    registrar_envio_transferencia_con_validaciones,
    revisar_transferencia_con_validaciones,
)

transferencias_bp = Blueprint("transferencias", __name__)


@transferencias_bp.get("/listar_transferencias")
def listar_transferencias_endpoint():
    """Lista transferencias y su estado de atencion."""
    return jsonify({"data": listar_transferencias_para_respuesta()}), 200


@transferencias_bp.get("/obtener_transferencia/<int:id_transferencia>")
def obtener_transferencia_endpoint(id_transferencia):
    """Consulta una transferencia por id."""
    transferencia = obtener_transferencia_para_respuesta(id_transferencia)
    if not transferencia:
        return jsonify({"message": "Transferencia no encontrada."}), 404

    return jsonify({"data": transferencia}), 200


@transferencias_bp.post("/crear_transferencia")
def crear_transferencia_endpoint():
    """Registra la solicitud de transferencia entre sucursales."""
    datos = request.get_json(silent=True) or {}
    transferencia, errores = crear_transferencia_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear la transferencia.", "errors": errores}), 400

    return jsonify({
        "message": "Transferencia solicitada correctamente.",
        "data": transferencia,
    }), 201


@transferencias_bp.post("/revisar_transferencia/<int:id_transferencia>")
def revisar_transferencia_endpoint(id_transferencia):
    """Aprueba, ajusta o rechaza una solicitud desde la sucursal origen."""
    datos = request.get_json(silent=True) or {}
    transferencia, errores = revisar_transferencia_con_validaciones(id_transferencia, datos)

    if errores:
        return jsonify({"message": "No se pudo revisar la transferencia.", "errors": errores}), 400

    return jsonify({
        "message": "Transferencia revisada correctamente.",
        "data": transferencia,
    }), 200


@transferencias_bp.post("/registrar_envio_transferencia/<int:id_transferencia>")
def registrar_envio_transferencia_endpoint(id_transferencia):
    """Registra el despacho y descuenta inventario de la sucursal origen."""
    datos = request.get_json(silent=True) or {}
    transferencia, envio, errores = registrar_envio_transferencia_con_validaciones(
        id_transferencia,
        datos,
    )

    if errores:
        return jsonify({"message": "No se pudo registrar el envio.", "errors": errores}), 400

    return jsonify({
        "message": "Envio de transferencia registrado correctamente.",
        "data": {
            "transferencia": transferencia,
            "envio": envio,
        },
    }), 200


@transferencias_bp.post("/confirmar_recepcion_transferencia/<int:id_transferencia>")
def confirmar_recepcion_transferencia_endpoint(id_transferencia):
    """Confirma recepcion completa o parcial y actualiza inventario destino."""
    datos = request.get_json(silent=True) or {}
    transferencia, recepcion, errores = confirmar_recepcion_transferencia_con_validaciones(
        id_transferencia,
        datos,
    )

    if errores:
        return jsonify({"message": "No se pudo confirmar la recepcion.", "errors": errores}), 400

    return jsonify({
        "message": "Recepcion de transferencia confirmada correctamente.",
        "data": {
            "transferencia": transferencia,
            "recepcion": recepcion,
        },
    }), 200
