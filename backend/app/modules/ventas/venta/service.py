from datetime import datetime

from app.extensions import db
from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_por_sucursal_y_producto_en_bd,
)
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.precio_producto.repository import (
    consultar_precio_por_producto_y_lista_en_bd,
)
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.inventario.producto_unidad.repository import consultar_producto_unidad_por_id_en_bd
from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_tipo_movimiento_inventario_por_nombre_en_bd,
)
from app.modules.inventario.lista_precio.repository import consultar_lista_precio_por_id_en_bd
from app.modules.sucursales.sucursal.repository import consultar_sucursal_por_id_en_bd
from app.modules.ventas.cliente.repository import consultar_cliente_por_id_en_bd
from app.modules.ventas.detalle_venta.model import DetalleVenta
from app.modules.ventas.venta.model import Venta
from app.modules.ventas.venta.repository import (
    consultar_todas_las_ventas_en_bd,
    consultar_venta_por_id_en_bd,
)
from app.modules.ventas.venta.schema import (
    convertir_valor_a_decimal,
    convertir_venta_a_respuesta,
    validar_datos_para_crear_venta,
)


def listar_ventas_para_respuesta(filtros=None):
    """Consulta ventas y las deja listas para API."""
    ventas = consultar_todas_las_ventas_en_bd(filtros)
    return [convertir_venta_a_respuesta(venta) for venta in ventas]


def obtener_venta_para_respuesta(id_venta):
    """Consulta una venta por id y la deja lista para responder."""
    venta = consultar_venta_por_id_en_bd(id_venta)
    if not venta:
        return None

    return convertir_venta_a_respuesta(venta)


def crear_venta_con_validaciones(datos):
    """Registra una venta confirmada siguiendo el flujo de venta documentado."""
    errores = validar_datos_para_crear_venta(datos)
    if errores:
        return None, errores

    errores_relaciones = validar_relaciones_de_venta(datos)
    if errores_relaciones:
        return None, errores_relaciones

    detalles, inventarios, descuento_total, total, errores_stock = preparar_detalles_de_venta(datos)
    if errores_stock:
        return None, errores_stock

    tipo_salida = consultar_tipo_movimiento_inventario_por_nombre_en_bd("SALIDA")
    if not tipo_salida:
        return None, {"tipo_movimiento": "No existe el tipo de movimiento SALIDA."}

    try:
        venta = Venta(
            id_sucursal=datos["id_sucursal"],
            id_usuario=datos["id_usuario"],
            id_cliente=datos.get("id_cliente"),
            id_lista_precio=datos["id_lista_precio"],
            fecha=datetime.utcnow(),
            descuento_total=descuento_total,
            total=total,
            comprobante="PENDIENTE",
            estado="CONFIRMADA",
            detalles=detalles,
        )
        db.session.add(venta)
        db.session.flush()

        venta.comprobante = generar_comprobante_venta(venta)
        actualizar_inventario_y_movimientos_por_venta(
            venta,
            inventarios,
            tipo_salida.id_tipo_movimiento,
        )

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return convertir_venta_a_respuesta(venta), None


def validar_relaciones_de_venta(datos):
    """Valida sucursal, usuario, cliente opcional, lista de precios y productos."""
    errores = {}

    if not consultar_sucursal_por_id_en_bd(datos["id_sucursal"]):
        errores["id_sucursal"] = "No existe una sucursal con ese id."

    if not consultar_usuario_por_id_en_bd(datos["id_usuario"]):
        errores["id_usuario"] = "No existe usuario con ese id."

    if datos.get("id_cliente") and not consultar_cliente_por_id_en_bd(datos["id_cliente"]):
        errores["id_cliente"] = "No existe cliente con ese id."

    lista_precio = consultar_lista_precio_por_id_en_bd(datos["id_lista_precio"])
    if not lista_precio:
        errores["id_lista_precio"] = "No existe una lista de precios con ese id."
    elif not lista_precio.activa:
        errores["id_lista_precio"] = "La lista de precios no esta activa."

    for posicion, detalle in enumerate(datos["detalles"], start=1):
        producto = consultar_producto_por_id_en_bd(detalle["id_producto"])
        producto_unidad = consultar_producto_unidad_por_id_en_bd(detalle["id_producto_unidad"])

        if not producto:
            errores[f"detalle_{posicion}_id_producto"] = "No existe un producto con ese id."
        elif not producto.activo:
            errores[f"detalle_{posicion}_id_producto"] = "El producto no esta activo."

        if not producto_unidad:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "No existe una unidad asociada a producto con ese id."
            )
        elif producto_unidad.id_producto != detalle["id_producto"]:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "La unidad indicada no pertenece al producto del detalle."
            )
        elif not producto_unidad.activo:
            errores[f"detalle_{posicion}_id_producto_unidad"] = (
                "La unidad indicada no esta activa."
            )

    return errores


def preparar_detalles_de_venta(datos):
    """Valida stock, aplica precios/descuentos y construye los detalles."""
    detalles = []
    inventarios = {}
    descuento_total = convertir_valor_a_decimal(0)
    total = convertir_valor_a_decimal(0)
    errores = {}

    for posicion, detalle_recibido in enumerate(datos["detalles"], start=1):
        id_producto = detalle_recibido["id_producto"]
        id_producto_unidad = detalle_recibido["id_producto_unidad"]
        cantidad = convertir_valor_a_decimal(detalle_recibido["cantidad"])
        descuento = convertir_valor_a_decimal(detalle_recibido.get("descuento", 0))
        prefijo = f"detalle_{posicion}"

        producto_unidad = consultar_producto_unidad_por_id_en_bd(id_producto_unidad)
        factor_conversion = convertir_valor_a_decimal(producto_unidad.factor_conversion)
        cantidad_base = cantidad * factor_conversion

        precio = consultar_precio_por_producto_y_lista_en_bd(
            id_producto,
            datos["id_lista_precio"],
        )
        if not precio or not precio.activo:
            errores[f"{prefijo}_precio"] = (
                "El producto no tiene precio activo en la lista seleccionada."
            )
            continue

        # La lista de precios se interpreta como precio de unidad base.
        precio_unitario_aplicado = precio.precio * factor_conversion

        inventario = consultar_inventario_por_sucursal_y_producto_en_bd(
            datos["id_sucursal"],
            id_producto,
        )
        if not inventario:
            errores[f"{prefijo}_stock"] = "El producto no tiene inventario en esta sucursal."
            continue

        cantidad_total_producto = sumar_cantidad_producto_en_venta(
            datos["detalles"],
            id_producto,
        )
        if inventario.cantidad_actual < cantidad_total_producto:
            errores[f"{prefijo}_stock"] = (
                "Stock insuficiente para confirmar la venta de este producto."
            )
            continue

        subtotal_bruto = cantidad * precio_unitario_aplicado
        if descuento > subtotal_bruto:
            errores[f"{prefijo}_descuento"] = "El descuento no puede superar el subtotal."
            continue

        subtotal = subtotal_bruto - descuento
        detalle = DetalleVenta(
            id_producto=id_producto,
            id_producto_unidad=id_producto_unidad,
            cantidad=cantidad,
            precio_unitario=precio_unitario_aplicado,
            descuento=descuento,
            subtotal=subtotal,
        )

        detalles.append(detalle)
        inventarios[id_producto] = inventario
        descuento_total += descuento
        total += subtotal

    if errores:
        return None, None, None, None, errores

    return detalles, inventarios, descuento_total, total, None


def sumar_cantidad_producto_en_venta(detalles, id_producto):
    """Suma cantidades repetidas del mismo producto en unidad base."""
    total = convertir_valor_a_decimal(0)

    for detalle in detalles:
        if detalle["id_producto"] != id_producto:
            continue

        cantidad = convertir_valor_a_decimal(detalle["cantidad"])
        producto_unidad = consultar_producto_unidad_por_id_en_bd(
            detalle["id_producto_unidad"]
        )
        factor_conversion = convertir_valor_a_decimal(producto_unidad.factor_conversion)

        total += cantidad * factor_conversion

    return total


def actualizar_inventario_y_movimientos_por_venta(venta, inventarios, id_tipo_salida):
    """Descuenta stock y deja un movimiento SALIDA por cada detalle vendido."""
    for detalle in venta.detalles:
        inventario = inventarios[detalle.id_producto]

        factor_conversion = convertir_valor_a_decimal(
            detalle.producto_unidad.factor_conversion
        )
        cantidad_base = detalle.cantidad * factor_conversion

        inventario.cantidad_actual -= cantidad_base
        db.session.add(inventario)
        db.session.flush()

        movimiento = MovimientoInventario(
            id_inventario=inventario.id_inventario,
            id_usuario=venta.id_usuario,
            id_tipo_movimiento=id_tipo_salida,
            motivo=f"Venta {venta.comprobante}",
            cantidad=cantidad_base,
            modulo_origen="VENTA",
            id_origen=venta.id_venta,
        )
        db.session.add(movimiento)


def generar_comprobante_venta(venta):
    """Genera un consecutivo legible para sustentar la venta registrada."""
    fecha = venta.fecha.strftime("%Y%m%d")
    return f"VTA-{fecha}-{venta.id_venta:06d}"
