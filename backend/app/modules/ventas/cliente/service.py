from app.modules.ventas.cliente.model import Cliente
from app.modules.ventas.cliente.repository import (
    consultar_cliente_por_documento_en_bd,
    consultar_cliente_por_id_en_bd,
    consultar_todos_los_clientes_en_bd,
    guardar_cliente_en_base_de_datos,
)
from app.modules.ventas.cliente.schema import (
    convertir_cliente_a_respuesta,
    validar_datos_para_guardar_cliente,
)
from app.modules.ventas.tipo_documento.repository import (
    consultar_tipo_documento_por_id_en_bd,
)


def listar_clientes_para_respuesta():
    """Consulta clientes y los deja listos para responder por la API."""
    clientes = consultar_todos_los_clientes_en_bd()
    return [convertir_cliente_a_respuesta(cliente) for cliente in clientes]


def obtener_cliente_para_respuesta(id_cliente):
    """Consulta un cliente por id y lo deja listo para responder por la API."""
    cliente = consultar_cliente_por_id_en_bd(id_cliente)
    if not cliente:
        return None

    return convertir_cliente_a_respuesta(cliente)


def crear_cliente_con_validaciones(datos):
    """Valida datos, evita documento duplicado y crea el cliente en PostgreSQL."""
    errores = validar_datos_para_guardar_cliente(datos)
    if errores:
        return None, errores

    numero_documento = datos["numero_documento"].strip()
    if consultar_cliente_por_documento_en_bd(numero_documento):
        return None, {"numero_documento": "Ya existe un cliente con ese documento."}

    tipo_documento, error_tipo_documento = resolver_tipo_documento_cliente(datos)
    if error_tipo_documento:
        return None, error_tipo_documento

    cliente = Cliente(
        id_tipo_documento=tipo_documento.id_tipo_documento,
        numero_documento=numero_documento,
        nombre=datos["nombre"].strip(),
        correo=(datos.get("correo") or "").strip() or None,
        telefono=(datos.get("telefono") or "").strip() or None,
        activo=datos.get("activo", True),
    )

    cliente_guardado = guardar_cliente_en_base_de_datos(cliente)
    return convertir_cliente_a_respuesta(cliente_guardado), None


def actualizar_cliente_con_validaciones(id_cliente, datos):
    """Valida datos y actualiza un cliente existente en PostgreSQL."""
    cliente = consultar_cliente_por_id_en_bd(id_cliente)
    if not cliente:
        return None, {"cliente": "No existe un cliente con ese id."}

    errores = validar_datos_para_guardar_cliente(datos)
    if errores:
        return None, errores

    numero_documento = datos["numero_documento"].strip()
    cliente_existente = consultar_cliente_por_documento_en_bd(numero_documento)
    if cliente_existente and cliente_existente.id_cliente != cliente.id_cliente:
        return None, {"numero_documento": "Ya existe otro cliente con ese documento."}

    tipo_documento, error_tipo_documento = resolver_tipo_documento_cliente(datos)
    if error_tipo_documento:
        return None, error_tipo_documento

    cliente.id_tipo_documento = tipo_documento.id_tipo_documento
    cliente.numero_documento = numero_documento
    cliente.nombre = datos["nombre"].strip()
    cliente.correo = (datos.get("correo") or "").strip() or None
    cliente.telefono = (datos.get("telefono") or "").strip() or None
    cliente.activo = datos.get("activo", cliente.activo)

    cliente_guardado = guardar_cliente_en_base_de_datos(cliente)
    return convertir_cliente_a_respuesta(cliente_guardado), None


def resolver_tipo_documento_cliente(datos):
    """Resuelve el tipo de documento del cliente por FK."""
    tipo_documento = consultar_tipo_documento_por_id_en_bd(datos["id_tipo_documento"])
    if not tipo_documento:
        return None, {"id_tipo_documento": "No existe un tipo de documento con ese id."}

    if not tipo_documento.activo:
        return None, {"id_tipo_documento": "El tipo de documento no esta activo."}

    return tipo_documento, None
