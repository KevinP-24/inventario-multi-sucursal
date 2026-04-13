from app.modules.inventario.lista_precio.repository import consultar_lista_precio_por_id_en_bd
from app.modules.inventario.precio_producto.model import PrecioProducto
from app.modules.inventario.precio_producto.repository import (
    consultar_precio_por_producto_y_lista_en_bd,
    consultar_precio_producto_por_id_en_bd,
    consultar_todos_los_precios_producto_en_bd,
    guardar_precio_producto_en_base_de_datos,
)
from app.modules.inventario.precio_producto.schema import (
    convertir_precio_producto_a_respuesta,
    convertir_texto_a_fecha,
    convertir_valor_a_decimal,
    validar_datos_para_guardar_precio_producto,
)
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd


def listar_precios_producto_para_respuesta():
    """Consulta precios de productos y los deja listos para responder por API."""
    precios = consultar_todos_los_precios_producto_en_bd()
    return [convertir_precio_producto_a_respuesta(precio) for precio in precios]


def obtener_precio_producto_para_respuesta(id_precio_producto):
    """Consulta un precio de producto por id y lo deja listo para responder."""
    precio = consultar_precio_producto_por_id_en_bd(id_precio_producto)
    if not precio:
        return None

    return convertir_precio_producto_a_respuesta(precio)


def crear_precio_producto_con_validaciones(datos):
    """Valida datos y crea el precio de un producto en una lista."""
    errores = validar_datos_para_guardar_precio_producto(datos)
    if errores:
        return None, errores

    if not consultar_producto_por_id_en_bd(datos["id_producto"]):
        return None, {"id_producto": "El producto indicado no existe."}

    if not consultar_lista_precio_por_id_en_bd(datos["id_lista_precio"]):
        return None, {"id_lista_precio": "La lista de precio indicada no existe."}

    if consultar_precio_por_producto_y_lista_en_bd(datos["id_producto"], datos["id_lista_precio"]):
        return None, {"precio_producto": "Ese producto ya tiene precio en esa lista."}

    precio_producto = PrecioProducto(
        id_producto=datos["id_producto"],
        id_lista_precio=datos["id_lista_precio"],
        precio=convertir_valor_a_decimal(datos["precio"]),
        fecha_vigencia=convertir_texto_a_fecha(datos.get("fecha_vigencia")),
        activo=datos.get("activo", True),
    )

    precio_guardado = guardar_precio_producto_en_base_de_datos(precio_producto)
    return convertir_precio_producto_a_respuesta(precio_guardado), None


def actualizar_precio_producto_con_validaciones(id_precio_producto, datos):
    """Valida datos y actualiza un precio de producto existente."""
    precio_producto = consultar_precio_producto_por_id_en_bd(id_precio_producto)
    if not precio_producto:
        return None, {"precio_producto": "No existe un precio de producto con ese id."}

    errores = validar_datos_para_guardar_precio_producto(datos)
    if errores:
        return None, errores

    if not consultar_producto_por_id_en_bd(datos["id_producto"]):
        return None, {"id_producto": "El producto indicado no existe."}

    if not consultar_lista_precio_por_id_en_bd(datos["id_lista_precio"]):
        return None, {"id_lista_precio": "La lista de precio indicada no existe."}

    precio_existente = consultar_precio_por_producto_y_lista_en_bd(
        datos["id_producto"],
        datos["id_lista_precio"],
    )
    if precio_existente and precio_existente.id_precio_producto != precio_producto.id_precio_producto:
        return None, {"precio_producto": "Otro registro ya usa ese producto con esa lista."}

    precio_producto.id_producto = datos["id_producto"]
    precio_producto.id_lista_precio = datos["id_lista_precio"]
    precio_producto.precio = convertir_valor_a_decimal(datos["precio"])
    precio_producto.fecha_vigencia = convertir_texto_a_fecha(datos.get("fecha_vigencia"))
    precio_producto.activo = datos.get("activo", precio_producto.activo)

    precio_guardado = guardar_precio_producto_en_base_de_datos(precio_producto)
    return convertir_precio_producto_a_respuesta(precio_guardado), None
