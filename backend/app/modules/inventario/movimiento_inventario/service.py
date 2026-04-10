from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_sucursal_por_id_en_bd,
)
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.movimiento_inventario.repository import (
    consultar_movimiento_inventario_por_id_en_bd,
    consultar_movimientos_por_inventario_en_bd,
    consultar_todos_los_movimientos_inventario_en_bd,
    filtrar_movimientos_inventario_en_bd,
    guardar_movimiento_inventario_en_base_de_datos,
)
from app.modules.inventario.movimiento_inventario.schema import (
    convertir_movimiento_inventario_a_respuesta,
    convertir_texto_a_fecha_hora_para_filtro,
    convertir_texto_a_fecha_hora,
    convertir_valor_a_decimal,
    validar_datos_para_registrar_movimiento_inventario,
)
from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_tipo_movimiento_inventario_por_id_en_bd,
)


def listar_movimientos_inventario_para_respuesta():
    """Consulta todo el historial de inventario y lo deja listo para API."""
    movimientos = consultar_todos_los_movimientos_inventario_en_bd()
    return [convertir_movimiento_inventario_a_respuesta(item) for item in movimientos]


def obtener_movimiento_inventario_para_respuesta(id_movimiento):
    """Consulta un movimiento por id y lo deja listo para responder."""
    movimiento = consultar_movimiento_inventario_por_id_en_bd(id_movimiento)
    if not movimiento:
        return None

    return convertir_movimiento_inventario_a_respuesta(movimiento)


def listar_movimientos_por_inventario_para_respuesta(id_inventario):
    """Consulta el historial de un inventario especifico."""
    movimientos = consultar_movimientos_por_inventario_en_bd(id_inventario)
    return [convertir_movimiento_inventario_a_respuesta(item) for item in movimientos]


def filtrar_movimientos_inventario_para_respuesta(parametros):
    """Filtra historial de inventario por campos usados en auditoria."""
    filtros, errores = construir_filtros_de_movimientos(parametros)
    if errores:
        return None, errores

    movimientos = filtrar_movimientos_inventario_en_bd(filtros)
    return [convertir_movimiento_inventario_a_respuesta(item) for item in movimientos], None


def construir_filtros_de_movimientos(parametros):
    """Convierte query params de Flask en filtros tipados para SQLAlchemy."""
    errores = {}
    filtros = {
        "id_inventario": parametros.get("id_inventario", type=int),
        "id_sucursal": parametros.get("id_sucursal", type=int),
        "id_producto": parametros.get("id_producto", type=int),
        "id_usuario": parametros.get("id_usuario", type=int),
        "id_tipo_movimiento": parametros.get("id_tipo_movimiento", type=int),
        "id_origen": parametros.get("id_origen", type=int),
    }

    tipo_movimiento = (parametros.get("tipo_movimiento") or "").strip().upper()
    if tipo_movimiento:
        filtros["tipo_movimiento"] = tipo_movimiento

    modulo_origen = (parametros.get("modulo_origen") or "").strip().upper()
    if modulo_origen:
        filtros["modulo_origen"] = modulo_origen

    fecha_desde_texto = parametros.get("fecha_desde")
    fecha_hasta_texto = parametros.get("fecha_hasta")
    filtros["fecha_desde"] = convertir_texto_a_fecha_hora_para_filtro(fecha_desde_texto)
    filtros["fecha_hasta"] = convertir_texto_a_fecha_hora_para_filtro(
        fecha_hasta_texto,
        es_fecha_hasta=True,
    )

    if fecha_desde_texto and filtros["fecha_desde"] is None:
        errores["fecha_desde"] = "La fecha desde debe tener formato YYYY-MM-DD o ISO."

    if fecha_hasta_texto and filtros["fecha_hasta"] is None:
        errores["fecha_hasta"] = "La fecha hasta debe tener formato YYYY-MM-DD o ISO."

    return filtros, errores


def registrar_movimiento_inventario_con_validaciones(datos):
    """Registra una entrada/salida en el historial sin cambiar el stock actual.

    Las compras, ventas y transferencias se encargan de cambiar
    inventario_sucursal. Despues llaman esta funcion para dejar el rastro.
    """
    errores = validar_datos_para_registrar_movimiento_inventario(datos)
    if errores:
        return None, errores

    id_inventario = datos["id_inventario"]
    id_usuario = datos["id_usuario"]
    id_tipo_movimiento = datos["id_tipo_movimiento"]

    if not consultar_inventario_sucursal_por_id_en_bd(id_inventario):
        return None, {"id_inventario": "No existe inventario con ese id."}

    if not consultar_usuario_por_id_en_bd(id_usuario):
        return None, {"id_usuario": "No existe usuario con ese id."}

    if not consultar_tipo_movimiento_inventario_por_id_en_bd(id_tipo_movimiento):
        return None, {"id_tipo_movimiento": "No existe un tipo de movimiento con ese id."}

    movimiento = MovimientoInventario(
        id_inventario=id_inventario,
        id_usuario=id_usuario,
        id_tipo_movimiento=id_tipo_movimiento,
        motivo=(datos.get("motivo") or "").strip() or None,
        cantidad=convertir_valor_a_decimal(datos.get("cantidad")),
        fecha_hora=convertir_texto_a_fecha_hora(datos.get("fecha_hora")),
        modulo_origen=(datos.get("modulo_origen") or "").strip() or None,
        id_origen=datos.get("id_origen"),
    )

    movimiento_guardado = guardar_movimiento_inventario_en_base_de_datos(movimiento)
    return convertir_movimiento_inventario_a_respuesta(movimiento_guardado), None
