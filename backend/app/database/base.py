"""Importa los modelos que Alembic debe conocer.

Cuando generemos migraciones, Flask-Migrate revisa los modelos cargados en
SQLAlchemy. Por eso este archivo centraliza los imports de las entidades que
ya existen en codigo.
"""

from app.modules.compras.proveedor.model import Proveedor
from app.modules.compras.orden_compra.model import OrdenCompra
from app.modules.compras.detalle_orden_compra.model import DetalleOrdenCompra
from app.modules.admin.parametro_sistema.model import ParametroSistema
from app.modules.auth.rol.model import Rol
from app.modules.auth.usuario.model import Usuario
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.lista_precio.model import ListaPrecio
from app.modules.inventario.movimiento_inventario.model import MovimientoInventario
from app.modules.inventario.precio_producto.model import PrecioProducto
from app.modules.inventario.producto.model import Producto
from app.modules.inventario.producto_unidad.model import ProductoUnidad
from app.modules.inventario.tipo_movimiento_inventario.model import TipoMovimientoInventario
from app.modules.inventario.unidad_medida.model import UnidadMedida
from app.modules.logistica.ruta_logistica.model import RutaLogistica
from app.modules.logistica.transportista.model import Transportista
from app.modules.sucursales.sucursal.model import Sucursal
from app.modules.ventas.cliente.model import Cliente

__all__ = [
    "Rol",
    "Usuario",
    "Sucursal",
    "Cliente",
    "UnidadMedida",
    "Producto",
    "ProductoUnidad",
    "InventarioSucursal",
    "TipoMovimientoInventario",
    "MovimientoInventario",
    "Proveedor",
    "OrdenCompra",
    "DetalleOrdenCompra",
    "ListaPrecio",
    "PrecioProducto",
    "Transportista",
    "RutaLogistica",
    "ParametroSistema",
]
