from datetime import date

from app.extensions import db
from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.modules.compras.detalle_orden_compra.model import DetalleOrdenCompra
from app.modules.compras.orden_compra.model import OrdenCompra
from app.modules.compras.orden_compra.repository import (
    consultar_orden_compra_por_id_en_bd,
    consultar_todas_las_ordenes_compra_en_bd,
    filtrar_ordenes_compra_en_bd,
    guardar_orden_compra_en_base_de_datos,
)
from app.modules.compras.orden_compra.schema import (
    construir_filtros_historial_compras,
    convertir_orden_compra_a_respuesta,
    convertir_texto_a_fecha,
    convertir_valor_a_decimal,
    validar_datos_para_crear_orden_compra,
    validar_datos_para_recibir_orden_compra,
)
from app.modules.compras.proveedor.repository import consultar_proveedor_por_id_en_bd
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_por_sucursal_y_producto_en_bd,
)
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.inventario.producto_unidad.repository import consultar_producto_unidad_por_id_en_bd
from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_tipo_movimiento_inventario_por_nombre_en_bd,
)
from app.modules.sucursales.sucursal.repository import consultar_sucursal_por_id_en_bd


def listar_ordenes_compra_para_respuesta():
    """Consulta ordenes de compra y las deja listas para API."""
    ordenes = consultar_todas_las_ordenes_compra_en_bd()
    return [convertir_orden_compra_a_respuesta(orden) for orden in ordenes]


def obtener_orden_compra_para_respuesta(id_orden_compra):
    """Consulta una orden de compra por id y la deja lista para responder."""
    orden = consultar_orden_compra_por_id_en_bd(id_orden_compra)
    if not orden:
        return None

    return convertir_orden_compra_a_respuesta(orden)


def filtrar_historial_compras_para_respuesta(parametros):
    """Consulta compras historicas por proveedor, producto, sucursal, estado o fechas."""
    filtros, errores = construir_filtros_historial_compras(parametros)
    if errores:
        return None, errores

    ordenes = filtrar_ordenes_compra_en_bd(filtros)
    return [convertir_orden_compra_a_respuesta(orden) for orden in ordenes], None


def crear_orden_compra_con_validaciones(datos):
    """Crea una orden con detalles y calcula los totales automaticamente."""
    errores = validar_datos_para_crear_orden_compra(datos)
    if errores:
        return None, errores

    errores_relaciones = validar_relaciones_de_orden_compra(datos)
    if errores_relaciones:
        return None, errores_relaciones

    detalles, subtotal, descuento_total, total = construir_detalles_y_totales(datos["detalles"])

    orden = OrdenCompra(
        id_proveedor=datos["id_proveedor"],
        id_sucursal=datos["id_sucursal"],
        id_usuario=datos["id_usuario"],
        fecha=convertir_texto_a_fecha(datos.get("fecha")),
        estado="CREADA",
        plazo_pago=(datos.get("plazo_pago") or "").strip() or None,
        subtotal=subtotal,
        descuento_total=descuento_total,
        total=total,
        detalles=detalles,
    )

    orden_guardada = guardar_orden_compra_en_base_de_datos(orden)
    return convertir_orden_compra_a_respuesta(orden_guardada), None


def anular_orden_compra_con_validaciones(id_orden_compra):
    """Anula una orden registrada si todavia no fue recibida."""
    orden = consultar_orden_compra_por_id_en_bd(id_orden_compra)
    if not orden:
        return None, {"orden_compra": "No existe una orden de compra con ese id."}

    if orden.estado == "RECIBIDA":
        return None, {"estado": "No se puede anular una orden de compra ya recibida."}

    if orden.estado == "ANULADA":
        return None, {"estado": "La orden de compra ya se encuentra anulada."}

    orden.estado = "ANULADA"
    orden_guardada = guardar_orden_compra_en_base_de_datos(orden)
    return convertir_orden_compra_a_respuesta(orden_guardada), None


def recibir_orden_compra_con_validaciones(id_orden_compra, datos):
    """Recibe una orden y registra el ingreso de sus productos al inventario."""
    errores = validar_datos_para_recibir_orden_compra(datos)
    if errores:
        return None, None, errores

    orden = consultar_orden_compra_por_id_en_bd(id_orden_compra)
    if not orden:
        return None, None, {"orden_compra": "No existe una orden de compra con ese id."}

    if orden.estado != "CREADA":
        return None, None, {
            "estado": "La orden solo puede recibirse cuando esta en estado CREADA."
        }

    id_usuario_recepcion = datos["id_usuario_recepcion"]
    if not consultar_usuario_por_id_en_bd(id_usuario_recepcion):
        return None, None, {"id_usuario_recepcion": "No existe usuario con ese id."}

    tipo_entrada = consultar_tipo_movimiento_inventario_por_nombre_en_bd("ENTRADA")
    if not tipo_entrada:
        return None, None, {
            "tipo_movimiento": "No existe el tipo de movimiento ENTRADA."
        }

    if not orden.detalles:
        return None, None, {"detalles": "La orden no tiene productos para recibir."}

    try:
        movimientos = registrar_entrada_de_compra_en_inventario(
            orden,
            id_usuario_recepcion,
            tipo_entrada.id_tipo_movimiento,
        )

        orden.estado = "RECIBIDA"
        orden.fecha_recepcion = date.today()
        orden.id_usuario_recepcion = id_usuario_recepcion

        db.session.add(orden)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return (
        convertir_orden_compra_a_respuesta(orden),
        [movimiento.convertir_a_diccionario() for movimiento in movimientos],
        None,
    )


def registrar_entrada_de_compra_en_inventario(orden, id_usuario_recepcion, id_tipo_movimiento):
    """Suma el stock comprado y deja un movimiento por cada detalle recibido."""
    movimientos = []

    for detalle in orden.detalles:
        factor_conversion = convertir_valor_a_decimal(
            detalle.producto_unidad.factor_conversion
        )
        cantidad_base = detalle.cantidad * factor_conversion
        costo_unitario_base = detalle.subtotal / cantidad_base

        inventario = consultar_inventario_por_sucursal_y_producto_en_bd(
            orden.id_sucursal,
            detalle.id_producto,
        )

        if not inventario:
            inventario = InventarioSucursal(
                id_sucursal=orden.id_sucursal,
                id_producto=detalle.id_producto,
                cantidad_actual=0,
                costo_promedio=costo_unitario_base,
            )

        inventario.costo_promedio = calcular_costo_promedio_ponderado(
            inventario.cantidad_actual,
            inventario.costo_promedio,
            cantidad_base,
            costo_unitario_base,
        )
        inventario.cantidad_actual += cantidad_base
        db.session.add(inventario)

        if detalle.producto:
            detalle.producto.ultimo_costo_compra = costo_unitario_base
            db.session.add(detalle.producto)

        db.session.flush()

        movimiento = MovimientoInventario(
            id_inventario=inventario.id_inventario,
            id_usuario=id_usuario_recepcion,
            id_tipo_movimiento=id_tipo_movimiento,
            motivo="Recepcion de orden de compra",
            cantidad=cantidad_base,
            modulo_origen="COMPRA",
            id_origen=orden.id_orden_compra,
        )
        db.session.add(movimiento)
        movimientos.append(movimiento)

    db.session.flush()
    return movimientos


def calcular_costo_promedio_ponderado(
    cantidad_actual,
    costo_promedio_actual,
    cantidad_comprada,
    costo_unitario_compra,
):
    """Calcula el nuevo costo promedio al recibir mercancia comprada."""
    cantidad_total = cantidad_actual + cantidad_comprada
    if cantidad_total <= 0:
        return costo_unitario_compra

    valor_actual = cantidad_actual * costo_promedio_actual
    valor_compra = cantidad_comprada * costo_unitario_compra
    return (valor_actual + valor_compra) / cantidad_total


def validar_relaciones_de_orden_compra(datos):
    """Valida que proveedor, sucursal, usuario, productos y unidades existan."""
    errores = {}

    if not consultar_proveedor_por_id_en_bd(datos["id_proveedor"]):
        errores["id_proveedor"] = "No existe un proveedor con ese id."

    if not consultar_sucursal_por_id_en_bd(datos["id_sucursal"]):
        errores["id_sucursal"] = "No existe una sucursal con ese id."

    if not consultar_usuario_por_id_en_bd(datos["id_usuario"]):
        errores["id_usuario"] = "No existe un usuario con ese id."

    for posicion, detalle in enumerate(datos["detalles"], start=1):
        producto = consultar_producto_por_id_en_bd(detalle["id_producto"])
        producto_unidad = consultar_producto_unidad_por_id_en_bd(detalle["id_producto_unidad"])

        if not producto:
            errores[f"detalle_{posicion}_id_producto"] = "No existe un producto con ese id."

        if not producto_unidad:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "No existe una unidad asociada a producto con ese id."
            )
        elif producto_unidad.id_producto != detalle["id_producto"]:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "La unidad indicada no pertenece al producto del detalle."
            )

    return errores


def construir_detalles_y_totales(detalles_recibidos):
    """Construye los detalles y suma subtotal, descuentos y total."""
    detalles = []
    subtotal_orden = convertir_valor_a_decimal(0)
    descuento_total = convertir_valor_a_decimal(0)
    total_orden = convertir_valor_a_decimal(0)

    for detalle_recibido in detalles_recibidos:
        cantidad = convertir_valor_a_decimal(detalle_recibido["cantidad"])
        precio_unitario = convertir_valor_a_decimal(detalle_recibido["precio_unitario"])
        descuento = convertir_valor_a_decimal(detalle_recibido.get("descuento", 0))

        producto_unidad = consultar_producto_unidad_por_id_en_bd(
            detalle_recibido["id_producto_unidad"]
        )
        factor_conversion = convertir_valor_a_decimal(producto_unidad.factor_conversion)

        # cantidad en unidad base
        cantidad_base = cantidad * factor_conversion

        # precio total bruto de la linea (precio_unitario viene en la unidad seleccionada)
        subtotal_bruto = cantidad * precio_unitario

        # descuento por unidad base -> descuento total de la linea
        descuento_total_detalle = descuento * cantidad_base

        subtotal_detalle = subtotal_bruto - descuento_total_detalle

        detalle = DetalleOrdenCompra(
            id_producto=detalle_recibido["id_producto"],
            id_producto_unidad=detalle_recibido["id_producto_unidad"],
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            descuento=descuento,   # se guarda el descuento unitario
            subtotal=subtotal_detalle,
        )

        detalles.append(detalle)
        subtotal_orden += subtotal_bruto
        descuento_total += descuento_total_detalle
        total_orden += subtotal_detalle

    return detalles, subtotal_orden, descuento_total, total_orden
