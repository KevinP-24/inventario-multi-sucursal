from app.modules.inventario.inventario_sucursal import inventario_sucursal_bp
from app.modules.inventario.lista_precio import listas_precio_bp
from app.modules.inventario.movimiento_inventario import movimientos_inventario_bp
from app.modules.inventario.precio_producto import precios_producto_bp
from app.modules.inventario.producto import productos_bp
from app.modules.inventario.producto_unidad import producto_unidades_bp
from app.modules.inventario.tipo_movimiento_inventario import tipos_movimiento_inventario_bp
from app.modules.inventario.unidad_medida import unidades_medida_bp

__all__ = [
    "productos_bp",
    "unidades_medida_bp",
    "producto_unidades_bp",
    "inventario_sucursal_bp",
    "movimientos_inventario_bp",
    "tipos_movimiento_inventario_bp",
    "listas_precio_bp",
    "precios_producto_bp",
]
