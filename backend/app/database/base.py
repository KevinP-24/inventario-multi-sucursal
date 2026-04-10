"""Importa los modelos que Alembic debe conocer.

Cuando generemos migraciones, Flask-Migrate revisa los modelos cargados en
SQLAlchemy. Por eso este archivo centraliza los imports de las entidades que
ya existen en codigo.
"""

from app.modules.auth.rol.model import Rol
from app.modules.auth.usuario.model import Usuario
from app.modules.inventario.producto.model import Producto
from app.modules.inventario.unidad_medida.model import UnidadMedida
from app.modules.sucursales.sucursal.model import Sucursal
from app.modules.ventas.cliente.model import Cliente

__all__ = ["Rol", "Usuario", "Sucursal", "Cliente", "UnidadMedida", "Producto"]
