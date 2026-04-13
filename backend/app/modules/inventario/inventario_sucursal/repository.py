from app.extensions import db
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.producto.model import Producto


def consultar_todo_el_inventario_sucursal_en_bd():
    """Consulta en PostgreSQL todo el stock por sucursal y producto."""
    return (
        InventarioSucursal.query
        .order_by(InventarioSucursal.id_sucursal.asc(), InventarioSucursal.id_producto.asc())
        .all()
    )


def consultar_inventario_sucursal_por_id_en_bd(id_inventario):
    """Consulta en PostgreSQL un registro de inventario por su id."""
    return InventarioSucursal.query.get(id_inventario)


def consultar_inventario_por_sucursal_y_producto_en_bd(id_sucursal, id_producto):
    """Consulta si ya existe stock registrado para esa sucursal y producto."""
    return InventarioSucursal.query.filter_by(
        id_sucursal=id_sucursal,
        id_producto=id_producto,
    ).first()


def consultar_alertas_stock_bajo_en_bd(id_sucursal=None):
    """Consulta productos cuyo stock actual esta igual o por debajo del minimo."""
    consulta = (
        InventarioSucursal.query
        .join(Producto, InventarioSucursal.id_producto == Producto.id_producto)
        .filter(Producto.activo.is_(True))
        .filter(InventarioSucursal.cantidad_actual <= Producto.stock_minimo)
    )

    if id_sucursal:
        consulta = consulta.filter(InventarioSucursal.id_sucursal == id_sucursal)

    return (
        consulta
        .order_by(InventarioSucursal.id_sucursal.asc(), Producto.nombre.asc())
        .all()
    )


def guardar_inventario_sucursal_en_base_de_datos(inventario):
    """Inserta o actualiza el stock actual en PostgreSQL."""
    db.session.add(inventario)
    db.session.commit()
    return inventario
