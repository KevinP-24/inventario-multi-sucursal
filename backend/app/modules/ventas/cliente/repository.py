from app.extensions import db
from app.modules.ventas.cliente.model import Cliente


def consultar_todos_los_clientes_en_bd():
    """Consulta en PostgreSQL todos los clientes ordenados por nombre."""
    return Cliente.query.order_by(Cliente.nombre.asc()).all()


def consultar_cliente_por_id_en_bd(id_cliente):
    """Consulta en PostgreSQL un cliente usando su id."""
    return Cliente.query.get(id_cliente)


def consultar_cliente_por_documento_en_bd(numero_documento):
    """Consulta en PostgreSQL si ya existe un cliente con ese documento."""
    return Cliente.query.filter_by(numero_documento=numero_documento).first()


def guardar_cliente_en_base_de_datos(cliente):
    """Inserta o actualiza un cliente en PostgreSQL."""
    db.session.add(cliente)
    db.session.commit()
    return cliente
