from app.modules.auth.rol.repository import (
    consultar_rol_por_nombre_en_bd,
    guardar_rol_en_base_de_datos,
)
from app.modules.auth.rol.schema import ROLES_BASE
from app.modules.auth.usuario.model import Usuario
from app.modules.auth.usuario.repository import (
    consultar_usuario_por_correo_en_bd,
    guardar_usuario_en_base_de_datos,
)
from app.modules.inventario.producto.model import Producto
from app.modules.inventario.producto.repository import (
    consultar_producto_por_codigo_en_bd,
    guardar_producto_en_base_de_datos,
)
from app.modules.inventario.producto.schema import PRODUCTOS_BASE
from app.modules.inventario.unidad_medida.model import UnidadMedida
from app.modules.inventario.unidad_medida.repository import (
    consultar_unidad_medida_por_simbolo_en_bd,
    guardar_unidad_medida_en_base_de_datos,
)
from app.modules.inventario.unidad_medida.schema import UNIDADES_MEDIDA_BASE
from app.modules.sucursales.sucursal.model import Sucursal
from app.modules.sucursales.sucursal.repository import (
    consultar_sucursal_por_nombre_en_bd,
    guardar_sucursal_en_base_de_datos,
)
from app.modules.sucursales.sucursal.schema import SUCURSALES_BASE
from app.security.password import generar_hash_password


USUARIOS_BASE = [
    {
        "nombre": "Admin General Demo",
        "correo": "admin.general@multisucursal.local",
        "password": "Admin123*",
        "rol": "Admin general",
        "sucursal": None,
    },
    {
        "nombre": "Admin Sucursal Demo",
        "correo": "admin.sucursal@multisucursal.local",
        "password": "Sucursal123*",
        "rol": "Admin sucursal",
        "sucursal": "Sucursal Centro Tecnologico",
    },
    {
        "nombre": "Operario Inventario Demo",
        "correo": "operario.inventario@multisucursal.local",
        "password": "Inventario123*",
        "rol": "Operario de inventario",
        "sucursal": "Sucursal Centro Tecnologico",
    },
]


def crear_roles_base_si_no_existen():
    """Crea los roles principales si todavia no estan en la base de datos.

    Este seeder es seguro para ejecutar muchas veces: primero consulta si el
    rol existe y solo lo inserta cuando hace falta.
    """
    roles_listos = []

    for datos_rol in ROLES_BASE:
        rol = consultar_rol_por_nombre_en_bd(datos_rol["nombre"])

        if not rol:
            from app.modules.auth.rol.model import Rol

            rol = Rol(**datos_rol)
            guardar_rol_en_base_de_datos(rol)

        roles_listos.append(rol)

    return roles_listos


def crear_sucursales_base_si_no_existen():
    """Crea sucursales demo para poder sustentar el alcance por sede."""
    sucursales_listas = []

    for datos_sucursal in SUCURSALES_BASE:
        sucursal = consultar_sucursal_por_nombre_en_bd(datos_sucursal["nombre"])

        if not sucursal:
            sucursal = Sucursal(**datos_sucursal)
            guardar_sucursal_en_base_de_datos(sucursal)

        sucursales_listas.append(sucursal)

    return sucursales_listas


def crear_usuarios_base_si_no_existen():
    """Crea usuarios demo para sustentar los tres roles principales.

    No actualizamos usuarios existentes para evitar sorpresas: si el correo ya
    existe, lo dejamos tal como esta en la base de datos.
    """
    usuarios_listos = []

    for datos_usuario in USUARIOS_BASE:
        usuario = consultar_usuario_por_correo_en_bd(datos_usuario["correo"])

        if not usuario:
            rol = consultar_rol_por_nombre_en_bd(datos_usuario["rol"])
            sucursal = None
            if datos_usuario["sucursal"]:
                sucursal = consultar_sucursal_por_nombre_en_bd(datos_usuario["sucursal"])

            usuario = Usuario(
                id_rol=rol.id_rol,
                id_sucursal=sucursal.id_sucursal if sucursal else None,
                nombre=datos_usuario["nombre"],
                correo=datos_usuario["correo"],
                password_hash=generar_hash_password(datos_usuario["password"]),
                activo=True,
            )
            guardar_usuario_en_base_de_datos(usuario)
        elif datos_usuario["sucursal"] and usuario.id_sucursal is None:
            # Si el usuario ya existia de una version anterior, solo completamos
            # la sucursal demo. No cambiamos nombre, correo ni contrasena.
            sucursal = consultar_sucursal_por_nombre_en_bd(datos_usuario["sucursal"])
            usuario.id_sucursal = sucursal.id_sucursal
            guardar_usuario_en_base_de_datos(usuario)

        usuarios_listos.append(usuario)

    return usuarios_listos


def crear_unidades_medida_base_si_no_existen():
    """Crea unidades de medida demo para poder registrar productos."""
    unidades_listas = []

    for datos_unidad in UNIDADES_MEDIDA_BASE:
        unidad = consultar_unidad_medida_por_simbolo_en_bd(datos_unidad["simbolo"])

        if not unidad:
            unidad = UnidadMedida(**datos_unidad)
            guardar_unidad_medida_en_base_de_datos(unidad)

        unidades_listas.append(unidad)

    return unidades_listas


def crear_productos_base_si_no_existen():
    """Crea productos demo para tener inventario inicial que mostrar."""
    productos_listos = []

    for datos_producto in PRODUCTOS_BASE:
        producto = consultar_producto_por_codigo_en_bd(datos_producto["codigo"])

        if not producto:
            producto = Producto(**datos_producto)
            guardar_producto_en_base_de_datos(producto)

        productos_listos.append(producto)

    return productos_listos


def ejecutar_seed_datos_base():
    """Ejecuta todos los datos iniciales que necesita el sistema para arrancar."""
    roles = crear_roles_base_si_no_existen()
    sucursales = crear_sucursales_base_si_no_existen()
    usuarios = crear_usuarios_base_si_no_existen()
    unidades_medida = crear_unidades_medida_base_si_no_existen()
    productos = crear_productos_base_si_no_existen()

    return {
        "roles": roles,
        "sucursales": sucursales,
        "usuarios": usuarios,
        "unidades_medida": unidades_medida,
        "productos": productos,
    }
