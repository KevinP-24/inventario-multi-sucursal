from app.extensions import db
from app.modules.ventas.venta.model import Venta


def consultar_todas_las_ventas_en_bd():
    """Consulta en PostgreSQL todas las ventas, de la mas reciente a la mas antigua."""
    return Venta.query.order_by(Venta.id_venta.desc()).all()


def consultar_venta_por_id_en_bd(id_venta):
    """Consulta en PostgreSQL una venta usando su id."""
    return Venta.query.get(id_venta)


def guardar_venta_en_base_de_datos(venta):
    """Inserta o actualiza una venta en PostgreSQL."""
    db.session.add(venta)
    db.session.commit()
    return venta
