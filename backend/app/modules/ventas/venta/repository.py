from app.extensions import db
from app.modules.ventas.venta.model import Venta


def consultar_todas_las_ventas_en_bd(filtros=None):
    """Consulta en PostgreSQL todas las ventas, de la mas reciente a la mas antigua."""
    query = Venta.query
    if filtros:
        if filtros.get("id_sucursal"):
            query = query.filter(Venta.id_sucursal == filtros["id_sucursal"])
        if filtros.get("id_cliente"):
            query = query.filter(Venta.id_cliente == filtros["id_cliente"])
        if filtros.get("fecha_inicio"):
            query = query.filter(Venta.fecha >= filtros["fecha_inicio"])
        if filtros.get("fecha_fin"):
            query = query.filter(Venta.fecha <= filtros["fecha_fin"])
            
    return query.order_by(Venta.id_venta.desc()).all()


def consultar_venta_por_id_en_bd(id_venta):
    """Consulta en PostgreSQL una venta usando su id."""
    return Venta.query.get(id_venta)


def guardar_venta_en_base_de_datos(venta):
    """Inserta o actualiza una venta en PostgreSQL."""
    db.session.add(venta)
    db.session.commit()
    return venta
