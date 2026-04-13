from app.extensions import db
from app.modules.compras.detalle_orden_compra.model import DetalleOrdenCompra


def consultar_detalles_por_orden_compra_en_bd(id_orden_compra):
    """Consulta todos los detalles de una orden de compra."""
    return DetalleOrdenCompra.query.filter_by(id_orden_compra=id_orden_compra).all()


def guardar_detalle_orden_compra_en_base_de_datos(detalle):
    """Inserta o actualiza un detalle de orden de compra en PostgreSQL."""
    db.session.add(detalle)
    db.session.commit()
    return detalle
