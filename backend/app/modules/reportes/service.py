from datetime import date, datetime

from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.producto.model import Producto
from app.modules.reportes.pdf import generar_pdf_tabular
from app.modules.transferencias.transferencia.model import Transferencia
from app.modules.ventas.venta.model import Venta


def generar_reporte_ventas_pdf(parametros):
    """Genera PDF de ventas filtrado por fecha y sucursal."""
    filtros, errores = construir_filtros_reportes(parametros)
    if errores:
        return None, None, errores

    consulta = Venta.query
    if filtros["id_sucursal"]:
        consulta = consulta.filter(Venta.id_sucursal == filtros["id_sucursal"])
    if filtros["fecha_desde"]:
        consulta = consulta.filter(Venta.fecha >= filtros["fecha_desde"])
    if filtros["fecha_hasta"]:
        consulta = consulta.filter(Venta.fecha <= filtros["fecha_hasta"])

    ventas = consulta.order_by(Venta.fecha.desc()).all()
    columnas = ["Fecha", "Sucursal", "Responsable", "Comprobante", "Estado", "Total"]
    filas = [
        [
            venta.fecha.strftime("%Y-%m-%d") if venta.fecha else "",
            venta.sucursal.nombre if venta.sucursal else venta.id_sucursal,
            venta.usuario.nombre if venta.usuario else venta.id_usuario,
            venta.comprobante,
            venta.estado,
            f"{float(venta.total):.2f}",
        ]
        for venta in ventas
    ]

    pdf = generar_pdf_tabular(
        "Reporte de ventas",
        construir_subtitulo_filtros(filtros),
        columnas,
        filas,
    )
    return pdf, "reporte_ventas.pdf", None


def generar_reporte_inventario_pdf(parametros):
    """Genera PDF de movimientos de inventario filtrado por fecha y sucursal."""
    filtros, errores = construir_filtros_reportes(parametros)
    if errores:
        return None, None, errores

    consulta = MovimientoInventario.query.join(
        InventarioSucursal,
        MovimientoInventario.id_inventario == InventarioSucursal.id_inventario,
    )
    if filtros["id_sucursal"]:
        consulta = consulta.filter(InventarioSucursal.id_sucursal == filtros["id_sucursal"])
    if filtros["fecha_desde"]:
        consulta = consulta.filter(MovimientoInventario.fecha_hora >= filtros["fecha_desde"])
    if filtros["fecha_hasta"]:
        consulta = consulta.filter(MovimientoInventario.fecha_hora <= filtros["fecha_hasta"])

    movimientos = consulta.order_by(MovimientoInventario.fecha_hora.desc()).all()
    columnas = ["Fecha", "Sucursal", "Producto", "Tipo", "Cantidad", "Motivo"]
    filas = [
        [
            movimiento.fecha_hora.strftime("%Y-%m-%d") if movimiento.fecha_hora else "",
            movimiento.inventario.sucursal.nombre if movimiento.inventario and movimiento.inventario.sucursal else "",
            movimiento.inventario.producto.nombre if movimiento.inventario and movimiento.inventario.producto else "",
            movimiento.tipo_movimiento.nombre if movimiento.tipo_movimiento else "",
            f"{float(movimiento.cantidad):.2f}",
            movimiento.motivo or "",
        ]
        for movimiento in movimientos
    ]

    pdf = generar_pdf_tabular(
        "Reporte de movimientos de inventario",
        construir_subtitulo_filtros(filtros),
        columnas,
        filas,
    )
    return pdf, "reporte_inventario.pdf", None


def generar_reporte_transferencias_pdf(parametros):
    """Genera PDF de transferencias filtrado por fecha y sucursal."""
    filtros, errores = construir_filtros_reportes(parametros)
    if errores:
        return None, None, errores

    consulta = Transferencia.query
    if filtros["id_sucursal"]:
        consulta = consulta.filter(
            (Transferencia.id_sucursal_origen == filtros["id_sucursal"])
            | (Transferencia.id_sucursal_destino == filtros["id_sucursal"])
        )
    if filtros["fecha_desde"]:
        consulta = consulta.filter(Transferencia.fecha_solicitud >= filtros["fecha_desde"])
    if filtros["fecha_hasta"]:
        consulta = consulta.filter(Transferencia.fecha_solicitud <= filtros["fecha_hasta"])

    transferencias = consulta.order_by(Transferencia.fecha_solicitud.desc()).all()
    columnas = ["Fecha", "Origen", "Destino", "Estado", "Prioridad", "Productos"]
    filas = [
        [
            transferencia.fecha_solicitud.strftime("%Y-%m-%d")
            if transferencia.fecha_solicitud
            else "",
            transferencia.sucursal_origen.nombre if transferencia.sucursal_origen else "",
            transferencia.sucursal_destino.nombre if transferencia.sucursal_destino else "",
            transferencia.estado_transferencia.nombre if transferencia.estado_transferencia else "",
            transferencia.prioridad,
            len(transferencia.detalles),
        ]
        for transferencia in transferencias
    ]

    pdf = generar_pdf_tabular(
        "Reporte de transferencias",
        construir_subtitulo_filtros(filtros),
        columnas,
        filas,
    )
    return pdf, "reporte_transferencias.pdf", None


def construir_filtros_reportes(parametros):
    """Valida filtros comunes para exportacion PDF."""
    errores = {}
    fecha_desde = convertir_fecha_inicio(parametros.get("fecha_desde"))
    fecha_hasta = convertir_fecha_fin(parametros.get("fecha_hasta"))

    if parametros.get("fecha_desde") and fecha_desde is None:
        errores["fecha_desde"] = "La fecha desde debe tener formato YYYY-MM-DD."
    if parametros.get("fecha_hasta") and fecha_hasta is None:
        errores["fecha_hasta"] = "La fecha hasta debe tener formato YYYY-MM-DD."
    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        errores["fechas"] = "La fecha desde no puede ser mayor que la fecha hasta."

    return {
        "id_sucursal": parametros.get("id_sucursal", type=int),
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
    }, errores


def convertir_fecha_inicio(valor):
    """Convierte YYYY-MM-DD a inicio de dia."""
    fecha = convertir_texto_a_fecha(valor)
    if not fecha:
        return None
    return datetime.combine(fecha, datetime.min.time())


def convertir_fecha_fin(valor):
    """Convierte YYYY-MM-DD a fin de dia."""
    fecha = convertir_texto_a_fecha(valor)
    if not fecha:
        return None
    return datetime.combine(fecha, datetime.max.time())


def convertir_texto_a_fecha(valor):
    """Convierte texto a fecha."""
    if not valor:
        return None
    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        return None


def construir_subtitulo_filtros(filtros):
    """Describe filtros aplicados en el PDF."""
    partes = []
    if filtros["id_sucursal"]:
        partes.append(f"Sucursal: {filtros['id_sucursal']}")
    if filtros["fecha_desde"]:
        partes.append(f"Desde: {filtros['fecha_desde'].date().isoformat()}")
    if filtros["fecha_hasta"]:
        partes.append(f"Hasta: {filtros['fecha_hasta'].date().isoformat()}")

    return " | ".join(partes) if partes else "Sin filtros aplicados"
