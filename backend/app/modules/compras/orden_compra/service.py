from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.modules.compras.detalle_orden_compra.model import DetalleOrdenCompra
from app.modules.compras.orden_compra.model import OrdenCompra
from app.modules.compras.orden_compra.repository import (
    consultar_orden_compra_por_id_en_bd,
    consultar_todas_las_ordenes_compra_en_bd,
    guardar_orden_compra_en_base_de_datos,
)
from app.modules.compras.orden_compra.schema import (
    convertir_orden_compra_a_respuesta,
    convertir_texto_a_fecha,
    convertir_valor_a_decimal,
    validar_datos_para_crear_orden_compra,
)
from app.modules.compras.proveedor.repository import consultar_proveedor_por_id_en_bd
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.inventario.producto_unidad.repository import consultar_producto_unidad_por_id_en_bd
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
        subtotal_bruto = cantidad * precio_unitario
        subtotal_detalle = subtotal_bruto - descuento

        detalle = DetalleOrdenCompra(
            id_producto=detalle_recibido["id_producto"],
            id_producto_unidad=detalle_recibido["id_producto_unidad"],
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            descuento=descuento,
            subtotal=subtotal_detalle,
        )

        detalles.append(detalle)
        subtotal_orden += subtotal_bruto
        descuento_total += descuento
        total_orden += subtotal_detalle

    return detalles, subtotal_orden, descuento_total, total_orden
