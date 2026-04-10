from decimal import Decimal, InvalidOperation


PRODUCTOS_BASE = [
    {
        "codigo": "PROD-001",
        "nombre": "Mouse inalambrico Logitech M185",
        "descripcion": "Periferico de tecnologia para ventas rapidas.",
        "stock_minimo": "12",
    },
    {
        "codigo": "PROD-002",
        "nombre": "Teclado mecanico Redragon Kumara",
        "descripcion": "Teclado gamer para inventario por unidades.",
        "stock_minimo": "8",
    },
    {
        "codigo": "PROD-003",
        "nombre": "Monitor Samsung 24 pulgadas",
        "descripcion": "Monitor para ventas empresariales y de mostrador.",
        "stock_minimo": "5",
    },
    {
        "codigo": "PROD-004",
        "nombre": "Limpiador de pantalla 1L",
        "descripcion": "Insumo liquido para mantenimiento de equipos.",
        "stock_minimo": "6",
    },
    {
        "codigo": "PROD-005",
        "nombre": "Pasta termica Arctic MX-4 4g",
        "descripcion": "Insumo tecnico para reparacion y mantenimiento.",
        "stock_minimo": "10",
    },
    {
        "codigo": "PROD-006",
        "nombre": "Cable HDMI 2 metros",
        "descripcion": "Cable de conexion para equipos y monitores.",
        "stock_minimo": "15",
    },
]


def convertir_valor_a_decimal(valor):
    """Convierte un valor recibido por API a Decimal para guardarlo bien."""
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError):
        return None


def validar_datos_para_guardar_producto(datos):
    """Valida los datos minimos antes de guardar un producto."""
    errores = {}

    if not (datos.get("codigo") or "").strip():
        errores["codigo"] = "El codigo del producto es obligatorio."

    if not (datos.get("nombre") or "").strip():
        errores["nombre"] = "El nombre del producto es obligatorio."

    stock_minimo = convertir_valor_a_decimal(datos.get("stock_minimo", 0))
    if stock_minimo is None:
        errores["stock_minimo"] = "El stock minimo debe ser numerico."
    elif stock_minimo < 0:
        errores["stock_minimo"] = "El stock minimo no puede ser negativo."

    return errores


def convertir_producto_a_respuesta(producto):
    """Convierte un producto SQLAlchemy a diccionario."""
    return producto.convertir_a_diccionario()
