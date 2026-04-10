from app.modules.inventario.producto.model import Producto
from app.modules.inventario.producto.repository import (
    consultar_producto_por_codigo_en_bd,
    consultar_producto_por_id_en_bd,
    consultar_todos_los_productos_en_bd,
    guardar_producto_en_base_de_datos,
)
from app.modules.inventario.producto.schema import (
    convertir_producto_a_respuesta,
    convertir_valor_a_decimal,
    validar_datos_para_guardar_producto,
)


def listar_productos_para_respuesta():
    """Consulta productos y los deja listos para responder por API."""
    productos = consultar_todos_los_productos_en_bd()
    return [convertir_producto_a_respuesta(producto) for producto in productos]


def obtener_producto_para_respuesta(id_producto):
    """Consulta un producto por id y lo deja listo para responder."""
    producto = consultar_producto_por_id_en_bd(id_producto)
    if not producto:
        return None

    return convertir_producto_a_respuesta(producto)


def crear_producto_con_validaciones(datos):
    """Valida datos, evita codigo duplicado y crea el producto en PostgreSQL."""
    errores = validar_datos_para_guardar_producto(datos)
    if errores:
        return None, errores

    codigo = datos["codigo"].strip().upper()
    if consultar_producto_por_codigo_en_bd(codigo):
        return None, {"codigo": "Ya existe un producto con ese codigo."}

    producto = Producto(
        codigo=codigo,
        nombre=datos["nombre"].strip(),
        descripcion=(datos.get("descripcion") or "").strip() or None,
        stock_minimo=convertir_valor_a_decimal(datos.get("stock_minimo", 0)),
        activo=datos.get("activo", True),
    )

    producto_guardado = guardar_producto_en_base_de_datos(producto)
    return convertir_producto_a_respuesta(producto_guardado), None


def actualizar_producto_con_validaciones(id_producto, datos):
    """Valida datos y actualiza un producto existente en PostgreSQL."""
    producto = consultar_producto_por_id_en_bd(id_producto)
    if not producto:
        return None, {"producto": "No existe un producto con ese id."}

    errores = validar_datos_para_guardar_producto(datos)
    if errores:
        return None, errores

    codigo = datos["codigo"].strip().upper()
    producto_con_codigo = consultar_producto_por_codigo_en_bd(codigo)
    if producto_con_codigo and producto_con_codigo.id_producto != producto.id_producto:
        return None, {"codigo": "Ya existe otro producto con ese codigo."}

    producto.codigo = codigo
    producto.nombre = datos["nombre"].strip()
    producto.descripcion = (datos.get("descripcion") or "").strip() or None
    producto.stock_minimo = convertir_valor_a_decimal(datos.get("stock_minimo", 0))
    producto.activo = datos.get("activo", producto.activo)

    producto_guardado = guardar_producto_en_base_de_datos(producto)
    return convertir_producto_a_respuesta(producto_guardado), None
