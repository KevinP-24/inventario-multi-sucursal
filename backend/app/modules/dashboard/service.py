from datetime import datetime
from types import SimpleNamespace

from sqlalchemy import extract, func

from app.extensions import db
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.producto.model import Producto
from app.modules.sucursales.sucursal.model import Sucursal
from app.modules.transferencias.detalle_transferencia.model import DetalleTransferencia
from app.modules.transferencias.estado_transferencia.model import EstadoTransferencia
from app.modules.transferencias.transferencia.model import Transferencia
from app.modules.ventas.detalle_venta.model import DetalleVenta
from app.modules.ventas.venta.model import Venta


def consultar_volumen_ventas_para_respuesta(id_sucursal=None, meses=6):
    """Compara el mes actual contra los meses anteriores disponibles."""
    meses = normalizar_limite(meses, minimo=1, maximo=24)
    consulta = (
        db.session.query(
            extract("year", Venta.fecha).label("anio"),
            extract("month", Venta.fecha).label("mes"),
            func.count(Venta.id_venta).label("cantidad_ventas"),
            func.coalesce(func.sum(Venta.total), 0).label("total_ventas"),
        )
        .filter(Venta.estado == "CONFIRMADA")
    )

    if id_sucursal:
        consulta = consulta.filter(Venta.id_sucursal == id_sucursal)

    filas = (
        consulta
        .group_by("anio", "mes")
        .order_by(db.desc("anio"), db.desc("mes"))
        .limit(meses)
        .all()
    )

    periodos = [
        {
            "anio": int(fila.anio),
            "mes": int(fila.mes),
            "periodo": f"{int(fila.anio):04d}-{int(fila.mes):02d}",
            "cantidad_ventas": int(fila.cantidad_ventas),
            "total_ventas": float(fila.total_ventas),
        }
        for fila in reversed(filas)
    ]

    hoy = datetime.utcnow()
    periodo_actual = f"{hoy.year:04d}-{hoy.month:02d}"
    actual = next(
        (periodo for periodo in periodos if periodo["periodo"] == periodo_actual),
        {
            "anio": hoy.year,
            "mes": hoy.month,
            "periodo": periodo_actual,
            "cantidad_ventas": 0,
            "total_ventas": 0,
        },
    )
    anteriores = [periodo for periodo in periodos if periodo["periodo"] != periodo_actual]
    promedio_anteriores = (
        sum(periodo["total_ventas"] for periodo in anteriores) / len(anteriores)
        if anteriores
        else 0
    )

    return {
        "mes_actual": actual,
        "promedio_periodos_anteriores": round(promedio_anteriores, 2),
        "variacion_frente_promedio": round(actual["total_ventas"] - promedio_anteriores, 2),
        "periodos": periodos,
    }


def consultar_rotacion_y_demanda_para_respuesta(id_sucursal=None, limite=10):
    """Calcula demanda por producto y una rotacion simple contra stock actual."""
    limite = normalizar_limite(limite)
    ventas_por_producto = consultar_ventas_por_producto(id_sucursal)
    inventarios = consultar_inventarios_para_dashboard(id_sucursal)

    indicadores = []
    productos_con_venta = {fila.id_producto for fila in ventas_por_producto}

    for fila in ventas_por_producto:
        inventario = inventarios.get(fila.id_producto)
        stock_actual = float(inventario.cantidad_actual) if inventario else 0
        cantidad_vendida = float(fila.cantidad_vendida)
        indicadores.append({
            "id_producto": fila.id_producto,
            "producto": fila.producto,
            "cantidad_vendida": cantidad_vendida,
            "stock_actual": stock_actual,
            "indice_rotacion": calcular_indice_rotacion(cantidad_vendida, stock_actual),
        })

    productos_sin_venta = [
        convertir_producto_sin_venta_a_indicador(inventario)
        for inventario in inventarios.values()
        if inventario.id_producto not in productos_con_venta
    ]

    alta_demanda = sorted(
        indicadores,
        key=lambda item: item["cantidad_vendida"],
        reverse=True,
    )[:limite]
    baja_demanda = sorted(
        indicadores + productos_sin_venta,
        key=lambda item: item["cantidad_vendida"],
    )[:limite]

    return {
        "productos_alta_demanda": alta_demanda,
        "productos_baja_demanda": baja_demanda,
        "rotacion_inventario": sorted(
            indicadores,
            key=lambda item: item["indice_rotacion"],
            reverse=True,
        )[:limite],
    }


def consultar_transferencias_activas_para_respuesta(id_sucursal=None):
    """Lista transferencias no finalizadas y resume cantidades con impacto operativo."""
    estados_activos = ["SOLICITADA", "APROBADA", "ENVIADA"]
    consulta = (
        Transferencia.query
        .join(
            EstadoTransferencia,
            Transferencia.id_estado_transferencia
            == EstadoTransferencia.id_estado_transferencia,
        )
        .filter(EstadoTransferencia.nombre.in_(estados_activos))
    )

    if id_sucursal:
        consulta = consulta.filter(
            (Transferencia.id_sucursal_origen == id_sucursal)
            | (Transferencia.id_sucursal_destino == id_sucursal)
        )

    transferencias = consulta.order_by(Transferencia.fecha_solicitud.desc()).all()
    return [
        convertir_transferencia_activa_a_indicador(transferencia)
        for transferencia in transferencias
    ]


def consultar_indicadores_reabastecimiento_para_respuesta(id_sucursal=None):
    """Consulta productos agotados, bajo minimo y proximos al minimo."""
    consulta = InventarioSucursal.query.join(
        Producto,
        InventarioSucursal.id_producto == Producto.id_producto,
    ).filter(Producto.activo.is_(True))

    if id_sucursal:
        consulta = consulta.filter(InventarioSucursal.id_sucursal == id_sucursal)

    indicadores = []
    for inventario in consulta.order_by(InventarioSucursal.id_sucursal.asc()).all():
        stock_minimo = float(inventario.producto.stock_minimo)
        cantidad_actual = float(inventario.cantidad_actual)
        umbral_proximo = stock_minimo * 1.25

        if cantidad_actual <= 0:
            estado = "AGOTADO"
        elif cantidad_actual <= stock_minimo:
            estado = "BAJO_MINIMO"
        elif cantidad_actual <= umbral_proximo:
            estado = "PROXIMO_A_AGOTARSE"
        else:
            continue

        indicadores.append({
            "id_sucursal": inventario.id_sucursal,
            "id_producto": inventario.id_producto,
            "producto": inventario.producto.nombre,
            "codigo_producto": inventario.producto.codigo,
            "cantidad_actual": cantidad_actual,
            "stock_minimo": stock_minimo,
            "cantidad_faltante": max(round(stock_minimo - cantidad_actual, 2), 0),
            "estado_reabastecimiento": estado,
        })

    return indicadores


def comparar_rendimiento_sucursales_para_respuesta():
    """Compara ventas, stock bajo y transferencias activas por sucursal."""
    sucursales = Sucursal.query.order_by(Sucursal.nombre.asc()).all()
    resultado = []

    for sucursal in sucursales:
        total_ventas = (
            db.session.query(func.coalesce(func.sum(Venta.total), 0))
            .filter(Venta.id_sucursal == sucursal.id_sucursal)
            .filter(Venta.estado == "CONFIRMADA")
            .scalar()
        )
        cantidad_ventas = (
            Venta.query
            .filter(Venta.id_sucursal == sucursal.id_sucursal)
            .filter(Venta.estado == "CONFIRMADA")
            .count()
        )
        productos_bajo_stock = len(
            consultar_indicadores_reabastecimiento_para_respuesta(sucursal.id_sucursal)
        )
        transferencias_activas = len(
            consultar_transferencias_activas_para_respuesta(sucursal.id_sucursal)
        )

        resultado.append({
            "id_sucursal": sucursal.id_sucursal,
            "sucursal": sucursal.nombre,
            "cantidad_ventas": cantidad_ventas,
            "total_ventas": float(total_ventas),
            "productos_bajo_stock": productos_bajo_stock,
            "transferencias_activas": transferencias_activas,
        })

    return sorted(resultado, key=lambda item: item["total_ventas"], reverse=True)


def consultar_ventas_por_producto(id_sucursal=None):
    """Agrupa unidades vendidas por producto."""
    consulta = (
        db.session.query(
            DetalleVenta.id_producto.label("id_producto"),
            Producto.nombre.label("producto"),
            func.coalesce(func.sum(DetalleVenta.cantidad), 0).label("cantidad_vendida"),
        )
        .join(Venta, DetalleVenta.id_venta == Venta.id_venta)
        .join(Producto, DetalleVenta.id_producto == Producto.id_producto)
        .filter(Venta.estado == "CONFIRMADA")
    )

    if id_sucursal:
        consulta = consulta.filter(Venta.id_sucursal == id_sucursal)

    return (
        consulta
        .group_by(DetalleVenta.id_producto, Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .all()
    )


def consultar_inventarios_para_dashboard(id_sucursal=None):
    """Obtiene un inventario representativo por producto para comparar demanda."""
    consulta = db.session.query(
        InventarioSucursal.id_producto.label("id_producto"),
        Producto.nombre.label("producto"),
        func.coalesce(func.sum(InventarioSucursal.cantidad_actual), 0).label("cantidad_actual"),
    ).join(
        Producto,
        InventarioSucursal.id_producto == Producto.id_producto,
    ).filter(Producto.activo.is_(True))

    if id_sucursal:
        consulta = consulta.filter(InventarioSucursal.id_sucursal == id_sucursal)

    filas = consulta.group_by(InventarioSucursal.id_producto, Producto.nombre).all()
    return {
        fila.id_producto: SimpleNamespace(
            id_producto=fila.id_producto,
            producto=SimpleNamespace(nombre=fila.producto),
            cantidad_actual=fila.cantidad_actual,
        )
        for fila in filas
    }


def convertir_producto_sin_venta_a_indicador(inventario):
    """Representa productos sin venta para detectar baja demanda."""
    stock_actual = float(inventario.cantidad_actual)
    return {
        "id_producto": inventario.id_producto,
        "producto": inventario.producto.nombre if inventario.producto else None,
        "cantidad_vendida": 0,
        "stock_actual": stock_actual,
        "indice_rotacion": 0,
    }


def convertir_transferencia_activa_a_indicador(transferencia):
    """Resume una transferencia activa y su cantidad comprometida."""
    cantidad_solicitada = sum(float(detalle.cantidad_solicitada) for detalle in transferencia.detalles)
    cantidad_aprobada = sum(float(detalle.cantidad_aprobada) for detalle in transferencia.detalles)
    cantidad_recibida = sum(float(detalle.cantidad_recibida) for detalle in transferencia.detalles)

    return {
        "id_transferencia": transferencia.id_transferencia,
        "estado": transferencia.estado_transferencia.nombre
        if transferencia.estado_transferencia
        else None,
        "id_sucursal_origen": transferencia.id_sucursal_origen,
        "id_sucursal_destino": transferencia.id_sucursal_destino,
        "fecha_solicitud": transferencia.fecha_solicitud.isoformat()
        if transferencia.fecha_solicitud
        else None,
        "cantidad_solicitada": cantidad_solicitada,
        "cantidad_aprobada": cantidad_aprobada,
        "cantidad_recibida": cantidad_recibida,
        "cantidad_pendiente": max(round(cantidad_aprobada - cantidad_recibida, 2), 0),
        "impacto_inventario": [
            convertir_detalle_transferencia_a_impacto(detalle)
            for detalle in transferencia.detalles
        ],
    }


def convertir_detalle_transferencia_a_impacto(detalle):
    """Expone el producto y las cantidades que afectan inventario."""
    return {
        "id_producto": detalle.id_producto,
        "producto": detalle.producto.nombre if detalle.producto else None,
        "cantidad_solicitada": float(detalle.cantidad_solicitada),
        "cantidad_aprobada": float(detalle.cantidad_aprobada),
        "cantidad_recibida": float(detalle.cantidad_recibida),
    }


def calcular_indice_rotacion(cantidad_vendida, stock_actual):
    """Calcula rotacion simple con stock actual como referencia."""
    if stock_actual <= 0:
        return round(cantidad_vendida, 2)

    return round(cantidad_vendida / stock_actual, 4)


def normalizar_limite(valor, minimo=1, maximo=50):
    """Mantiene limites razonables para respuestas de dashboard."""
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        valor = minimo

    return min(max(valor, minimo), maximo)
