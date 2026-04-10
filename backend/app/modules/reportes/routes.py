from io import BytesIO

from flask import Blueprint, jsonify, request, send_file

from app.modules.reportes.service import (
    generar_reporte_inventario_pdf,
    generar_reporte_transferencias_pdf,
    generar_reporte_ventas_pdf,
)

reportes_bp = Blueprint("reportes", __name__)


@reportes_bp.get("/ventas/pdf")
def reporte_ventas_pdf_endpoint():
    """Exporta ventas en PDF con filtros por fecha y sucursal."""
    return responder_pdf(generar_reporte_ventas_pdf(request.args))


@reportes_bp.get("/inventario/pdf")
def reporte_inventario_pdf_endpoint():
    """Exporta movimientos de inventario en PDF con filtros por fecha y sucursal."""
    return responder_pdf(generar_reporte_inventario_pdf(request.args))


@reportes_bp.get("/transferencias/pdf")
def reporte_transferencias_pdf_endpoint():
    """Exporta transferencias en PDF con filtros por fecha y sucursal."""
    return responder_pdf(generar_reporte_transferencias_pdf(request.args))


def responder_pdf(resultado):
    """Convierte bytes PDF en respuesta HTTP descargable."""
    pdf, nombre_archivo, errores = resultado
    if errores:
        return jsonify({"message": "No se pudo generar el reporte.", "errors": errores}), 400

    return send_file(
        BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nombre_archivo,
    )
