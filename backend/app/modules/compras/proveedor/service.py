from app.modules.compras.proveedor.model import Proveedor
from app.modules.compras.proveedor.repository import (
    consultar_proveedor_por_id_en_bd,
    consultar_proveedor_por_documento_en_bd,
    consultar_todos_los_proveedores_en_bd,
    guardar_proveedor_en_base_de_datos,
)
from app.modules.compras.proveedor.schema import (
    convertir_proveedor_a_respuesta,
    validar_datos_para_guardar_proveedor,
)
from app.modules.ventas.tipo_documento.repository import (
    consultar_tipo_documento_por_id_en_bd,
)


def listar_proveedores_para_respuesta():
    """Consulta proveedores y los deja listos para responder por API."""
    proveedores = consultar_todos_los_proveedores_en_bd()
    return [convertir_proveedor_a_respuesta(proveedor) for proveedor in proveedores]


def obtener_proveedor_para_respuesta(id_proveedor):
    """Consulta un proveedor por id y lo deja listo para responder."""
    proveedor = consultar_proveedor_por_id_en_bd(id_proveedor)
    if not proveedor:
        return None

    return convertir_proveedor_a_respuesta(proveedor)


def crear_proveedor_con_validaciones(datos):
    """Valida datos, evita documento duplicado y crea el proveedor."""
    errores = validar_datos_para_guardar_proveedor(datos)
    if errores:
        return None, errores

    numero_documento = datos["numero_documento"].strip()
    if consultar_proveedor_por_documento_en_bd(numero_documento):
        return None, {"numero_documento": "Ya existe un proveedor con ese documento."}

    tipo_documento, error_tipo_documento = resolver_tipo_documento_proveedor(datos)
    if error_tipo_documento:
        return None, error_tipo_documento

    proveedor = Proveedor(
        id_tipo_documento=tipo_documento.id_tipo_documento,
        numero_documento=numero_documento,
        nombre=datos["nombre"].strip(),
        correo=(datos.get("correo") or "").strip() or None,
        telefono=(datos.get("telefono") or "").strip() or None,
        direccion=(datos.get("direccion") or "").strip() or None,
        activo=datos.get("activo", True),
    )

    proveedor_guardado = guardar_proveedor_en_base_de_datos(proveedor)
    return convertir_proveedor_a_respuesta(proveedor_guardado), None


def actualizar_proveedor_con_validaciones(id_proveedor, datos):
    """Valida datos y actualiza un proveedor existente en PostgreSQL."""
    proveedor = consultar_proveedor_por_id_en_bd(id_proveedor)
    if not proveedor:
        return None, {"proveedor": "No existe un proveedor con ese id."}

    errores = validar_datos_para_guardar_proveedor(datos)
    if errores:
        return None, errores

    numero_documento = datos["numero_documento"].strip()
    proveedor_con_documento = consultar_proveedor_por_documento_en_bd(numero_documento)
    if proveedor_con_documento and proveedor_con_documento.id_proveedor != proveedor.id_proveedor:
        return None, {"numero_documento": "Ya existe otro proveedor con ese documento."}

    tipo_documento, error_tipo_documento = resolver_tipo_documento_proveedor(datos)
    if error_tipo_documento:
        return None, error_tipo_documento

    proveedor.id_tipo_documento = tipo_documento.id_tipo_documento
    proveedor.numero_documento = numero_documento
    proveedor.nombre = datos["nombre"].strip()
    proveedor.correo = (datos.get("correo") or "").strip() or None
    proveedor.telefono = (datos.get("telefono") or "").strip() or None
    proveedor.direccion = (datos.get("direccion") or "").strip() or None
    proveedor.activo = datos.get("activo", proveedor.activo)

    proveedor_guardado = guardar_proveedor_en_base_de_datos(proveedor)
    return convertir_proveedor_a_respuesta(proveedor_guardado), None


def resolver_tipo_documento_proveedor(datos):
    """Resuelve el tipo de documento del proveedor por FK."""
    tipo_documento = consultar_tipo_documento_por_id_en_bd(datos["id_tipo_documento"])
    if not tipo_documento:
        return None, {"id_tipo_documento": "No existe un tipo de documento con ese id."}

    if not tipo_documento.activo:
        return None, {"id_tipo_documento": "El tipo de documento no esta activo."}

    return tipo_documento, None
