from app.modules.inventario.lista_precio.model import ListaPrecio
from app.modules.inventario.lista_precio.repository import (
    consultar_lista_precio_por_id_en_bd,
    consultar_lista_precio_por_nombre_en_bd,
    consultar_todas_las_listas_precio_en_bd,
    guardar_lista_precio_en_base_de_datos,
)
from app.modules.inventario.lista_precio.schema import (
    convertir_lista_precio_a_respuesta,
    validar_datos_para_guardar_lista_precio,
)


def listar_listas_precio_para_respuesta():
    """Consulta listas de precio y las deja listas para responder por API."""
    listas = consultar_todas_las_listas_precio_en_bd()
    return [convertir_lista_precio_a_respuesta(lista) for lista in listas]


def obtener_lista_precio_para_respuesta(id_lista_precio):
    """Consulta una lista de precio por id y la deja lista para responder."""
    lista = consultar_lista_precio_por_id_en_bd(id_lista_precio)
    if not lista:
        return None

    return convertir_lista_precio_a_respuesta(lista)


def crear_lista_precio_con_validaciones(datos):
    """Valida datos, evita duplicados y crea la lista de precio."""
    errores = validar_datos_para_guardar_lista_precio(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    if consultar_lista_precio_por_nombre_en_bd(nombre):
        return None, {"nombre": "Ya existe una lista de precio con ese nombre."}

    lista = ListaPrecio(
        nombre=nombre,
        descripcion=(datos.get("descripcion") or "").strip() or None,
        activa=datos.get("activa", True),
    )

    lista_guardada = guardar_lista_precio_en_base_de_datos(lista)
    return convertir_lista_precio_a_respuesta(lista_guardada), None


def actualizar_lista_precio_con_validaciones(id_lista_precio, datos):
    """Valida datos y actualiza una lista de precio existente."""
    lista = consultar_lista_precio_por_id_en_bd(id_lista_precio)
    if not lista:
        return None, {"lista_precio": "No existe una lista de precio con ese id."}

    errores = validar_datos_para_guardar_lista_precio(datos)
    if errores:
        return None, errores

    nombre = datos["nombre"].strip()
    lista_existente = consultar_lista_precio_por_nombre_en_bd(nombre)
    if lista_existente and lista_existente.id_lista_precio != lista.id_lista_precio:
        return None, {"nombre": "Ya existe otra lista de precio con ese nombre."}

    lista.nombre = nombre
    lista.descripcion = (datos.get("descripcion") or "").strip() or None
    lista.activa = datos.get("activa", lista.activa)

    lista_guardada = guardar_lista_precio_en_base_de_datos(lista)
    return convertir_lista_precio_a_respuesta(lista_guardada), None
