from app.extensions import db
from app.modules.inventario.producto.model import Producto


def consultar_todos_los_productos_en_bd():
    """Consulta en PostgreSQL todos los productos ordenados por nombre."""
    return Producto.query.order_by(Producto.nombre.asc()).all()


def consultar_producto_por_id_en_bd(id_producto):
    """Consulta en PostgreSQL un producto usando su id."""
    return Producto.query.get(id_producto)


def consultar_producto_por_codigo_en_bd(codigo):
    """Consulta en PostgreSQL si ya existe un producto con ese codigo."""
    return Producto.query.filter_by(codigo=codigo).first()


def guardar_producto_en_base_de_datos(producto):
    """Inserta o actualiza un producto en PostgreSQL."""
    db.session.add(producto)
    db.session.commit()
    return producto
