from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_sucursal_por_id_en_bd,
)
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.movimiento_inventario.repository import (
    consultar_movimiento_inventario_por_id_en_bd,
    consultar_movimientos_por_inventario_en_bd,
    consultar_todos_los_movimientos_inventario_en_bd,
    guardar_movimiento_inventario_en_base_de_datos,
)
from app.modules.inventario.movimiento_inventario.schema import (
    convertir_movimiento_inventario_a_respuesta,
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
