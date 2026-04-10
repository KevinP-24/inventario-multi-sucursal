from app.extensions import db
from app.modules.inventario.lista_precio.model import ListaPrecio


def consultar_todas_las_listas_precio_en_bd():
    """Consulta en PostgreSQL todas las listas de precio ordenadas por nombre."""
    return ListaPrecio.query.order_by(ListaPrecio.nombre.asc()).all()


def consultar_lista_precio_por_id_en_bd(id_lista_precio):
    """Consulta en PostgreSQL una lista de precio usando su id."""
    return ListaPrecio.query.get(id_lista_precio)


def consultar_lista_precio_por_nombre_en_bd(nombre):
    """Consulta en PostgreSQL si ya existe una lista con ese nombre."""
    return ListaPrecio.query.filter_by(nombre=nombre).first()


def guardar_lista_precio_en_base_de_datos(lista_precio):
    """Inserta o actualiza una lista de precio en PostgreSQL."""
    db.session.add(lista_precio)
    db.session.commit()
    return lista_precio
