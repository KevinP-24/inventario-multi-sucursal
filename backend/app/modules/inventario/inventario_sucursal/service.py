from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_alertas_stock_bajo_en_bd,
    consultar_inventario_por_sucursal_y_producto_en_bd,
    consultar_inventario_sucursal_por_id_en_bd,
    consultar_todo_el_inventario_sucursal_en_bd,
    guardar_inventario_sucursal_en_base_de_datos,
)
from app.modules.inventario.inventario_sucursal.schema import (
    convertir_alerta_stock_bajo_a_respuesta,
    convertir_inventario_sucursal_a_respuesta,
    convertir_valor_a_decimal,
    validar_datos_para_ajustar_inventario_sucursal,
    validar_datos_para_guardar_inventario_sucursal,
    validar_datos_para_movimiento_operativo_inventario,
)
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_tipo_movimiento_inventario_por_nombre_en_bd,
)
from app.modules.sucursales.sucursal.repository import consultar_sucursal_por_id_en_bd
from app.modules.auth.usuario.repository import consultar_usuario_por_id_en_bd
from app.extensions import db


def listar_inventario_sucursal_para_respuesta():
    """Consulta todo el stock actual y lo deja listo para responder por API."""
    inventarios = consultar_todo_el_inventario_sucursal_en_bd()
    return [convertir_inventario_sucursal_a_respuesta(item) for item in inventarios]


def listar_alertas_stock_bajo_para_respuesta(id_sucursal=None):
    """Consulta productos que necesitan reabastecimiento segun su stock minimo."""
    inventarios = consultar_alertas_stock_bajo_en_bd(id_sucursal)
    return [convertir_alerta_stock_bajo_a_respuesta(item) for item in inventarios]


def obtener_inventario_sucursal_para_respuesta(id_inventario):
    """Consulta un registro de inventario por id y lo deja listo para responder."""
    inventario = consultar_inventario_sucursal_por_id_en_bd(id_inventario)
    if not inventario:
        return None

    return convertir_inventario_sucursal_a_respuesta(inventario)


def crear_inventario_sucursal_con_validaciones(datos):
    """Valida sucursal/producto y crea el stock inicial de ese producto."""
    errores = validar_datos_para_guardar_inventario_sucursal(datos)
    if errores:
        return None, errores

    id_sucursal = datos["id_sucursal"]
    id_producto = datos["id_producto"]

    if not consultar_sucursal_por_id_en_bd(id_sucursal):
        return None, {"id_sucursal": "No existe una sucursal con ese id."}

    if not consultar_producto_por_id_en_bd(id_producto):
        return None, {"id_producto": "No existe un producto con ese id."}

    if consultar_inventario_por_sucursal_y_producto_en_bd(id_sucursal, id_producto):
        return None, {
            "inventario_sucursal": "Ese producto ya tiene inventario registrado en esa sucursal."
        }

    inventario = InventarioSucursal(
        id_sucursal=id_sucursal,
        id_producto=id_producto,
        cantidad_actual=convertir_valor_a_decimal(datos.get("cantidad_actual", 0)),
        costo_promedio=convertir_valor_a_decimal(datos.get("costo_promedio", 0)),
    )

    inventario_guardado = guardar_inventario_sucursal_en_base_de_datos(inventario)
    return convertir_inventario_sucursal_a_respuesta(inventario_guardado), None


def actualizar_inventario_sucursal_con_validaciones(id_inventario, datos):
    """Actualiza cantidad actual y costo promedio de un registro existente."""
    inventario = consultar_inventario_sucursal_por_id_en_bd(id_inventario)
    if not inventario:
        return None, {"inventario_sucursal": "No existe inventario con ese id."}

    datos_para_validar = {
        "id_sucursal": inventario.id_sucursal,
        "id_producto": inventario.id_producto,
        "cantidad_actual": datos.get("cantidad_actual", inventario.cantidad_actual),
        "costo_promedio": datos.get("costo_promedio", inventario.costo_promedio),
    }
    errores = validar_datos_para_guardar_inventario_sucursal(datos_para_validar)
    if errores:
        return None, errores

    inventario.cantidad_actual = convertir_valor_a_decimal(datos_para_validar["cantidad_actual"])
    inventario.costo_promedio = convertir_valor_a_decimal(datos_para_validar["costo_promedio"])

    inventario_guardado = guardar_inventario_sucursal_en_base_de_datos(inventario)
    return convertir_inventario_sucursal_a_respuesta(inventario_guardado), None


def ajustar_inventario_sucursal_con_validaciones(id_inventario, datos):
    """Aplica una entrada, salida o ajuste manual y deja trazabilidad."""
    errores = validar_datos_para_ajustar_inventario_sucursal(datos)
    if errores:
        return None, None, errores

    inventario = consultar_inventario_sucursal_por_id_en_bd(id_inventario)
    if not inventario:
        return None, None, {"inventario_sucursal": "No existe inventario con ese id."}

    id_usuario = datos["id_usuario"]
    if not consultar_usuario_por_id_en_bd(id_usuario):
        return None, None, {"id_usuario": "No existe usuario con ese id."}

    tipo_ajuste = (datos.get("tipo_ajuste") or "").strip().upper()
    tipo_movimiento = consultar_tipo_movimiento_inventario_por_nombre_en_bd(tipo_ajuste)
    if not tipo_movimiento:
        return None, None, {"tipo_ajuste": "No existe ese tipo de movimiento de inventario."}

    cantidad_movimiento, cantidad_final, errores_stock = calcular_cambio_de_inventario(
        inventario,
        datos,
        tipo_ajuste,
    )
    if errores_stock:
        return None, None, errores_stock

    try:
        inventario.cantidad_actual = cantidad_final
        db.session.add(inventario)
        db.session.flush()

        movimiento = MovimientoInventario(
            id_inventario=inventario.id_inventario,
            id_usuario=id_usuario,
            id_tipo_movimiento=tipo_movimiento.id_tipo_movimiento,
            motivo=(datos.get("motivo") or "").strip() or "Ajuste operativo de inventario",
            cantidad=cantidad_movimiento,
            modulo_origen="AJUSTE_INVENTARIO",
            id_origen=inventario.id_inventario,
        )
        db.session.add(movimiento)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return (
        convertir_inventario_sucursal_a_respuesta(inventario),
        movimiento.convertir_a_diccionario(),
        None,
    )


def registrar_devolucion_inventario_con_validaciones(id_inventario, datos):
    """Registra una devolucion como entrada de stock con origen trazable."""
    return aplicar_movimiento_operativo_inventario(
        id_inventario=id_inventario,
        datos=datos,
        tipo_movimiento_nombre="ENTRADA",
        modulo_origen="DEVOLUCION",
        motivo_defecto="Devolucion de producto",
        suma_stock=True,
    )


def registrar_merma_inventario_con_validaciones(id_inventario, datos):
    """Registra una merma como salida de stock por perdida, dano o vencimiento."""
    return aplicar_movimiento_operativo_inventario(
        id_inventario=id_inventario,
        datos=datos,
        tipo_movimiento_nombre="SALIDA",
        modulo_origen="MERMA",
        motivo_defecto="Merma de inventario",
        suma_stock=False,
    )


def aplicar_movimiento_operativo_inventario(
    id_inventario,
    datos,
    tipo_movimiento_nombre,
    modulo_origen,
    motivo_defecto,
    suma_stock,
):
    """Aplica una devolucion o merma en una sola transaccion con movimiento."""
    errores = validar_datos_para_movimiento_operativo_inventario(datos)
    if errores:
        return None, None, errores

    inventario = consultar_inventario_sucursal_por_id_en_bd(id_inventario)
    if not inventario:
        return None, None, {"inventario_sucursal": "No existe inventario con ese id."}

    id_usuario = datos["id_usuario"]
    if not consultar_usuario_por_id_en_bd(id_usuario):
        return None, None, {"id_usuario": "No existe usuario con ese id."}

    tipo_movimiento = consultar_tipo_movimiento_inventario_por_nombre_en_bd(
        tipo_movimiento_nombre,
    )
    if not tipo_movimiento:
        return None, None, {
            "tipo_movimiento": "No existe ese tipo de movimiento de inventario."
        }

    cantidad = convertir_valor_a_decimal(datos.get("cantidad"))
    if not suma_stock and inventario.cantidad_actual < cantidad:
        return None, None, {"cantidad": "No hay stock suficiente para registrar la merma."}

    cantidad_final = inventario.cantidad_actual + cantidad
    if not suma_stock:
        cantidad_final = inventario.cantidad_actual - cantidad

    id_origen = datos.get("id_origen")
    if id_origen is not None:
        id_origen = int(id_origen)
    else:
        id_origen = inventario.id_inventario

    try:
        inventario.cantidad_actual = cantidad_final
        db.session.add(inventario)
        db.session.flush()

        movimiento = MovimientoInventario(
            id_inventario=inventario.id_inventario,
            id_usuario=id_usuario,
            id_tipo_movimiento=tipo_movimiento.id_tipo_movimiento,
            motivo=(datos.get("motivo") or "").strip() or motivo_defecto,
            cantidad=cantidad,
            modulo_origen=modulo_origen,
            id_origen=id_origen,
        )
        db.session.add(movimiento)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return (
        convertir_inventario_sucursal_a_respuesta(inventario),
        movimiento.convertir_a_diccionario(),
        None,
    )


def calcular_cambio_de_inventario(inventario, datos, tipo_ajuste):
    """Calcula la cantidad final y la cantidad que se registrara en historial."""
    cantidad_actual = inventario.cantidad_actual

    if tipo_ajuste == "ENTRADA":
        cantidad_movimiento = convertir_valor_a_decimal(datos.get("cantidad"))
        return cantidad_movimiento, cantidad_actual + cantidad_movimiento, None

    if tipo_ajuste == "SALIDA":
        cantidad_movimiento = convertir_valor_a_decimal(datos.get("cantidad"))
        if cantidad_actual < cantidad_movimiento:
            return None, None, {"cantidad": "No hay stock suficiente para registrar la salida."}

        return cantidad_movimiento, cantidad_actual - cantidad_movimiento, None

    cantidad_final = convertir_valor_a_decimal(datos.get("cantidad_actual_nueva"))
    diferencia = cantidad_final - cantidad_actual
    if diferencia == 0:
        return None, None, {
            "cantidad_actual_nueva": "La cantidad nueva debe ser diferente a la actual."
        }

    return abs(diferencia), cantidad_final, None
