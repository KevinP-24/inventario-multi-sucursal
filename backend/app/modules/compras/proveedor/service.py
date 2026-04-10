from app.modules.compras.proveedor.model import Proveedor
from app.modules.compras.proveedor.repository import (
    consultar_proveedor_por_id_en_bd,
    consultar_proveedor_por_nit_en_bd,
    consultar_todos_los_proveedores_en_bd,
    guardar_proveedor_en_base_de_datos,
)
from app.modules.compras.proveedor.schema import (
    convertir_proveedor_a_respuesta,
    validar_datos_para_guardar_proveedor,
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
    """Valida datos, evita NIT duplicado y crea el proveedor en PostgreSQL."""
    errores = validar_datos_para_guardar_proveedor(datos)
    if errores:
        return None, errores

    nit = datos["nit"].strip()
    if consultar_proveedor_por_nit_en_bd(nit):
        return None, {"nit": "Ya existe un proveedor con ese NIT."}

    proveedor = Proveedor(
        nit=nit,
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

    nit = datos["nit"].strip()
    proveedor_con_nit = consultar_proveedor_por_nit_en_bd(nit)
    if proveedor_con_nit and proveedor_con_nit.id_proveedor != proveedor.id_proveedor:
        return None, {"nit": "Ya existe otro proveedor con ese NIT."}

    proveedor.nit = nit
    proveedor.nombre = datos["nombre"].strip()
    proveedor.correo = (datos.get("correo") or "").strip() or None
    proveedor.telefono = (datos.get("telefono") or "").strip() or None
    proveedor.direccion = (datos.get("direccion") or "").strip() or None
    proveedor.activo = datos.get("activo", proveedor.activo)

    proveedor_guardado = guardar_proveedor_en_base_de_datos(proveedor)
    return convertir_proveedor_a_respuesta(proveedor_guardado), None
