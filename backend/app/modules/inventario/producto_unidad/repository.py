from app.extensions import db
from app.modules.inventario.producto_unidad.model import ProductoUnidad


def consultar_todas_las_producto_unidades_en_bd():
    """Consulta en PostgreSQL todas las relaciones producto-unidad."""
    return ProductoUnidad.query.order_by(ProductoUnidad.id_producto.asc()).all()


def consultar_producto_unidad_por_id_en_bd(id_producto_unidad):
    """Consulta en PostgreSQL una relacion producto-unidad usando su id."""
    return ProductoUnidad.query.get(id_producto_unidad)


def consultar_producto_unidad_por_producto_y_unidad_en_bd(id_producto, id_unidad):
    """Consulta si ya existe esa unidad para ese producto."""
    return ProductoUnidad.query.filter_by(
        id_producto=id_producto,
        id_unidad=id_unidad,
    ).first()


def guardar_producto_unidad_en_base_de_datos(producto_unidad):
    """Inserta o actualiza una relacion producto-unidad en PostgreSQL."""
    db.session.add(producto_unidad)
    db.session.commit()
    return producto_unidad
