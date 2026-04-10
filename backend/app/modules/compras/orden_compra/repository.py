from app.extensions import db
from app.modules.compras.orden_compra.model import OrdenCompra


def consultar_todas_las_ordenes_compra_en_bd():
    """Consulta en PostgreSQL todas las ordenes, de la mas reciente a la mas antigua."""
    return OrdenCompra.query.order_by(OrdenCompra.id_orden_compra.desc()).all()


def consultar_orden_compra_por_id_en_bd(id_orden_compra):
    """Consulta en PostgreSQL una orden de compra usando su id."""
    return OrdenCompra.query.get(id_orden_compra)


def guardar_orden_compra_en_base_de_datos(orden_compra):
    """Inserta o actualiza una orden de compra en PostgreSQL."""
    db.session.add(orden_compra)
    db.session.commit()
    return orden_compra
