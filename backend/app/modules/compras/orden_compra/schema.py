from datetime import date
from decimal import Decimal, InvalidOperation


ESTADOS_ORDEN_COMPRA = ["CREADA", "RECIBIDA", "ANULADA"]


def convertir_valor_a_decimal(valor):
    """Convierte valores monetarios o cantidades a Decimal."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def convertir_texto_a_fecha(valor):
    """Convierte una fecha YYYY-MM-DD; si viene vacia, usa la fecha actual."""
    if not valor:
        return date.today()

    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        return None


def validar_datos_para_crear_orden_compra(datos):
    """Valida cabecera y detalles antes de crear una orden de compra."""
    errores = {}

    if not datos.get("id_proveedor"):
        errores["id_proveedor"] = "El proveedor es obligatorio."

    if not datos.get("id_sucursal"):
        errores["id_sucursal"] = "La sucursal es obligatoria."

    if not datos.get("id_usuario"):
        errores["id_usuario"] = "El usuario que crea la orden es obligatorio."

    fecha = convertir_texto_a_fecha(datos.get("fecha"))
    if fecha is None:
        errores["fecha"] = "La fecha debe tener formato YYYY-MM-DD."

    detalles = datos.get("detalles") or []
    if not detalles:
        errores["detalles"] = "La orden necesita al menos un producto."

    for posicion, detalle in enumerate(detalles, start=1):
        validar_detalle_orden_compra(detalle, posicion, errores)

    return errores


def validar_datos_para_recibir_orden_compra(datos):
    """Valida los datos minimos para recibir una orden de compra."""
    errores = {}

    if not datos.get("id_usuario_recepcion"):
        errores["id_usuario_recepcion"] = "El usuario que recibe la orden es obligatorio."

    return errores


def validar_detalle_orden_compra(detalle, posicion, errores):
    """Valida una linea de detalle de la orden de compra."""
    prefijo = f"detalle_{posicion}"

    if not detalle.get("id_producto"):
        errores[f"{prefijo}_id_producto"] = "El producto es obligatorio."

    if not detalle.get("id_producto_unidad"):
        errores[f"{prefijo}_id_producto_unidad"] = "La unidad del producto es obligatoria."

    cantidad = convertir_valor_a_decimal(detalle.get("cantidad"))
    if cantidad is None:
        errores[f"{prefijo}_cantidad"] = "La cantidad debe ser numerica."
    elif cantidad <= 0:
        errores[f"{prefijo}_cantidad"] = "La cantidad debe ser mayor a cero."

    precio_unitario = convertir_valor_a_decimal(detalle.get("precio_unitario"))
    if precio_unitario is None:
        errores[f"{prefijo}_precio_unitario"] = "El precio unitario debe ser numerico."
    elif precio_unitario < 0:
        errores[f"{prefijo}_precio_unitario"] = "El precio unitario no puede ser negativo."

    descuento = convertir_valor_a_decimal(detalle.get("descuento", 0))
    if descuento is None:
        errores[f"{prefijo}_descuento"] = "El descuento debe ser numerico."
    elif descuento < 0:
        errores[f"{prefijo}_descuento"] = "El descuento no puede ser negativo."


def convertir_orden_compra_a_respuesta(orden_compra):
    """Convierte una orden SQLAlchemy a diccionario para responder por API."""
    return orden_compra.convertir_a_diccionario()
