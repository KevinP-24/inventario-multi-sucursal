from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_por_sucursal_y_producto_en_bd,
    consultar_inventario_sucursal_por_id_en_bd,
    consultar_todo_el_inventario_sucursal_en_bd,
    guardar_inventario_sucursal_en_base_de_datos,
)
from app.modules.inventario.inventario_sucursal.schema import (
    convertir_inventario_sucursal_a_respuesta,
    convertir_valor_a_decimal,
    validar_datos_para_guardar_inventario_sucursal,
)
from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.sucursales.sucursal.repository import consultar_sucursal_por_id_en_bd


def listar_inventario_sucursal_para_respuesta():
    """Consulta todo el stock actual y lo deja listo para responder por API."""
    inventarios = consultar_todo_el_inventario_sucursal_en_bd()
    return [convertir_inventario_sucursal_a_respuesta(item) for item in inventarios]


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
