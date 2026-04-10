from app.modules.inventario.producto.repository import consultar_producto_por_id_en_bd
from app.modules.inventario.producto_unidad.model import ProductoUnidad
from app.modules.inventario.producto_unidad.repository import (
    consultar_producto_unidad_por_id_en_bd,
    consultar_producto_unidad_por_producto_y_unidad_en_bd,
    consultar_todas_las_producto_unidades_en_bd,
    guardar_producto_unidad_en_base_de_datos,
)
from app.modules.inventario.producto_unidad.schema import (
    convertir_producto_unidad_a_respuesta,
    convertir_valor_a_decimal,
    validar_datos_para_guardar_producto_unidad,
)
from app.modules.inventario.unidad_medida.repository import consultar_unidad_medida_por_id_en_bd


def listar_producto_unidades_para_respuesta():
    """Consulta conversiones y las deja listas para responder por API."""
    conversiones = consultar_todas_las_producto_unidades_en_bd()
    return [convertir_producto_unidad_a_respuesta(conversion) for conversion in conversiones]


def obtener_producto_unidad_para_respuesta(id_producto_unidad):
    """Consulta una conversion por id y la deja lista para responder."""
    conversion = consultar_producto_unidad_por_id_en_bd(id_producto_unidad)
    if not conversion:
        return None

    return convertir_producto_unidad_a_respuesta(conversion)


def crear_producto_unidad_con_validaciones(datos):
    """Valida datos y crea una conversion producto-unidad en PostgreSQL."""
    errores = validar_datos_para_guardar_producto_unidad(datos)
    if errores:
        return None, errores

    producto = consultar_producto_por_id_en_bd(datos["id_producto"])
    if not producto:
        return None, {"id_producto": "El producto indicado no existe."}

    unidad = consultar_unidad_medida_por_id_en_bd(datos["id_unidad"])
    if not unidad:
        return None, {"id_unidad": "La unidad de medida indicada no existe."}

    if consultar_producto_unidad_por_producto_y_unidad_en_bd(datos["id_producto"], datos["id_unidad"]):
        return None, {"producto_unidad": "Ese producto ya tiene registrada esa unidad de medida."}

    producto_unidad = ProductoUnidad(
        id_producto=datos["id_producto"],
        id_unidad=datos["id_unidad"],
        factor_conversion=convertir_valor_a_decimal(datos.get("factor_conversion", 1)),
        es_base=datos.get("es_base", False),
        activo=datos.get("activo", True),
    )

    conversion_guardada = guardar_producto_unidad_en_base_de_datos(producto_unidad)
    return convertir_producto_unidad_a_respuesta(conversion_guardada), None


def actualizar_producto_unidad_con_validaciones(id_producto_unidad, datos):
    """Valida datos y actualiza una conversion producto-unidad existente."""
    conversion = consultar_producto_unidad_por_id_en_bd(id_producto_unidad)
    if not conversion:
        return None, {"producto_unidad": "No existe una conversion con ese id."}

    errores = validar_datos_para_guardar_producto_unidad(datos)
    if errores:
        return None, errores

    producto = consultar_producto_por_id_en_bd(datos["id_producto"])
    if not producto:
        return None, {"id_producto": "El producto indicado no existe."}

    unidad = consultar_unidad_medida_por_id_en_bd(datos["id_unidad"])
    if not unidad:
        return None, {"id_unidad": "La unidad de medida indicada no existe."}

    conversion_existente = consultar_producto_unidad_por_producto_y_unidad_en_bd(
        datos["id_producto"],
        datos["id_unidad"],
    )
    if conversion_existente and conversion_existente.id_producto_unidad != conversion.id_producto_unidad:
        return None, {"producto_unidad": "Otro registro ya usa ese producto con esa unidad."}

    conversion.id_producto = datos["id_producto"]
    conversion.id_unidad = datos["id_unidad"]
    conversion.factor_conversion = convertir_valor_a_decimal(datos.get("factor_conversion", 1))
    conversion.es_base = datos.get("es_base", conversion.es_base)
    conversion.activo = datos.get("activo", conversion.activo)

    conversion_guardada = guardar_producto_unidad_en_base_de_datos(conversion)
    return convertir_producto_unidad_a_respuesta(conversion_guardada), None
