from app.extensions import db
from app.modules.inventario.precio_producto.model import PrecioProducto


def consultar_todos_los_precios_producto_en_bd():
    """Consulta en PostgreSQL todos los precios de productos."""
    return PrecioProducto.query.order_by(PrecioProducto.id_producto.asc()).all()


def consultar_precio_producto_por_id_en_bd(id_precio_producto):
    """Consulta en PostgreSQL un precio de producto usando su id."""
    return PrecioProducto.query.get(id_precio_producto)


def consultar_precio_por_producto_y_lista_en_bd(id_producto, id_lista_precio):
    """Consulta si ya existe precio para ese producto en esa lista."""
    return PrecioProducto.query.filter_by(
        id_producto=id_producto,
        id_lista_precio=id_lista_precio,
    ).first()


def guardar_precio_producto_en_base_de_datos(precio_producto):
    """Inserta o actualiza un precio de producto en PostgreSQL."""
    db.session.add(precio_producto)
    db.session.commit()
    return precio_producto
