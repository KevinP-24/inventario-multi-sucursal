from app.modules.auth.rol.repository import (
    consultar_rol_por_nombre_en_bd,
    guardar_rol_en_base_de_datos,
)
from app.modules.admin.parametro_sistema.model import ParametroSistema
from app.modules.admin.parametro_sistema.repository import (
    consultar_parametro_sistema_por_clave_en_bd,
    guardar_parametro_sistema_en_base_de_datos,
)
from app.modules.admin.parametro_sistema.schema import PARAMETROS_SISTEMA_BASE
from app.modules.auth.rol.schema import ROLES_BASE
from app.modules.auth.usuario.model import Usuario
from app.modules.auth.usuario.repository import (
    consultar_usuario_por_correo_en_bd,
    guardar_usuario_en_base_de_datos,
)
from app.modules.compras.proveedor.model import Proveedor
from app.modules.compras.proveedor.repository import (
    consultar_proveedor_por_documento_en_bd,
    guardar_proveedor_en_base_de_datos,
)
from app.modules.compras.proveedor.schema import PROVEEDORES_BASE
from app.modules.inventario.producto.model import Producto
from app.modules.inventario.producto.repository import (
    consultar_producto_por_codigo_en_bd,
    guardar_producto_en_base_de_datos,
)
from app.modules.inventario.producto.schema import PRODUCTOS_BASE
from app.modules.inventario.inventario_sucursal.model import InventarioSucursal
from app.modules.inventario.inventario_sucursal.repository import (
    consultar_inventario_por_sucursal_y_producto_en_bd,
    guardar_inventario_sucursal_en_base_de_datos,
)
from app.modules.inventario.inventario_sucursal.schema import INVENTARIO_SUCURSAL_BASE
from app.modules.inventario.lista_precio.model import ListaPrecio
from app.modules.inventario.lista_precio.repository import (
    consultar_lista_precio_por_nombre_en_bd,
    guardar_lista_precio_en_base_de_datos,
)
from app.modules.inventario.lista_precio.schema import LISTAS_PRECIO_BASE
from app.modules.inventario.precio_producto.model import PrecioProducto
from app.modules.inventario.precio_producto.repository import (
    consultar_precio_por_producto_y_lista_en_bd,
    guardar_precio_producto_en_base_de_datos,
)
from app.modules.inventario.precio_producto.schema import PRECIOS_PRODUCTO_BASE
from app.modules.inventario.producto_unidad.model import ProductoUnidad
from app.modules.inventario.producto_unidad.repository import (
    consultar_producto_unidad_por_producto_y_unidad_en_bd,
    guardar_producto_unidad_en_base_de_datos,
)
from app.modules.inventario.producto_unidad.schema import PRODUCTO_UNIDADES_BASE
from app.modules.inventario.tipo_movimiento_inventario.model import TipoMovimientoInventario
from app.modules.inventario.tipo_movimiento_inventario.repository import (
    consultar_tipo_movimiento_inventario_por_nombre_en_bd,
    guardar_tipo_movimiento_inventario_en_base_de_datos,
)
from app.modules.inventario.tipo_movimiento_inventario.schema import (
    TIPOS_MOVIMIENTO_INVENTARIO_BASE,
)
from app.modules.transferencias.estado_transferencia.model import EstadoTransferencia
from app.modules.transferencias.estado_transferencia.repository import (
    consultar_estado_transferencia_por_nombre_en_bd,
    guardar_estado_transferencia_en_base_de_datos,
)
from app.modules.transferencias.estado_transferencia.schema import ESTADOS_TRANSFERENCIA_BASE
from app.modules.ventas.tipo_documento.model import TipoDocumento
from app.modules.ventas.tipo_documento.repository import (
    consultar_tipo_documento_por_codigo_en_bd,
    guardar_tipo_documento_en_base_de_datos,
)
from app.modules.ventas.tipo_documento.schema import TIPOS_DOCUMENTO_BASE
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
from app.modules.logistica.ruta_logistica.model import RutaLogistica
from app.modules.logistica.ruta_logistica.repository import (
    consultar_ruta_logistica_por_nombre_en_bd,
    guardar_ruta_logistica_en_base_de_datos,
)
from app.modules.logistica.ruta_logistica.schema import RUTAS_LOGISTICA_BASE
from app.modules.logistica.transportista.model import Transportista
from app.modules.logistica.transportista.repository import (
    consultar_transportista_por_identificacion_en_bd,
    guardar_transportista_en_base_de_datos,
)
from app.modules.logistica.transportista.schema import TRANSPORTISTAS_BASE
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


def crear_producto_unidades_base_si_no_existen():
    """Crea conversiones demo entre productos y unidades de medida."""
    conversiones_listas = []

    for datos_conversion in PRODUCTO_UNIDADES_BASE:
        producto = consultar_producto_por_codigo_en_bd(datos_conversion["codigo_producto"])
        unidad = consultar_unidad_medida_por_simbolo_en_bd(datos_conversion["simbolo_unidad"])

        conversion = consultar_producto_unidad_por_producto_y_unidad_en_bd(
            producto.id_producto,
            unidad.id_unidad,
        )

        if not conversion:
            conversion = ProductoUnidad(
                id_producto=producto.id_producto,
                id_unidad=unidad.id_unidad,
                factor_conversion=datos_conversion["factor_conversion"],
                es_base=datos_conversion["es_base"],
                activo=True,
            )
            guardar_producto_unidad_en_base_de_datos(conversion)

        conversiones_listas.append(conversion)

    return conversiones_listas


def crear_inventario_sucursal_base_si_no_existe():
    """Crea stock demo por sucursal y producto para arrancar la sustentacion.

    Solo inserta si no existe la combinacion sucursal/producto. Asi el seeder
    se puede ejecutar muchas veces sin pisar cantidades modificadas en pruebas.
    """
    inventarios_listos = []

    for datos_inventario in INVENTARIO_SUCURSAL_BASE:
        sucursal = consultar_sucursal_por_nombre_en_bd(datos_inventario["sucursal"])
        producto = consultar_producto_por_codigo_en_bd(datos_inventario["producto"])

        inventario = consultar_inventario_por_sucursal_y_producto_en_bd(
            sucursal.id_sucursal,
            producto.id_producto,
        )

        if not inventario:
            inventario = InventarioSucursal(
                id_sucursal=sucursal.id_sucursal,
                id_producto=producto.id_producto,
                cantidad_actual=datos_inventario["cantidad_actual"],
                costo_promedio=datos_inventario["costo_promedio"],
            )
            guardar_inventario_sucursal_en_base_de_datos(inventario)

        inventarios_listos.append(inventario)

    return inventarios_listos


def crear_tipos_movimiento_inventario_base_si_no_existen():
    """Crea el catalogo base para clasificar los movimientos de inventario."""
    tipos_listos = []

    for datos_tipo in TIPOS_MOVIMIENTO_INVENTARIO_BASE:
        tipo = consultar_tipo_movimiento_inventario_por_nombre_en_bd(datos_tipo["nombre"])

        if not tipo:
            tipo = TipoMovimientoInventario(**datos_tipo)
            guardar_tipo_movimiento_inventario_en_base_de_datos(tipo)

        tipos_listos.append(tipo)

    return tipos_listos


def crear_estados_transferencia_base_si_no_existen():
    """Crea el catalogo normalizado del ciclo de transferencias."""
    estados_listos = []

    for datos_estado in ESTADOS_TRANSFERENCIA_BASE:
        estado = consultar_estado_transferencia_por_nombre_en_bd(datos_estado["nombre"])

        if not estado:
            estado = EstadoTransferencia(**datos_estado)
            guardar_estado_transferencia_en_base_de_datos(estado)

        estados_listos.append(estado)

    return estados_listos


def crear_tipos_documento_base_si_no_existen():
    """Crea tipos de documento colombianos para clientes."""
    tipos_listos = []

    for datos_tipo in TIPOS_DOCUMENTO_BASE:
        tipo = consultar_tipo_documento_por_codigo_en_bd(datos_tipo["codigo"])

        if not tipo:
            tipo = TipoDocumento(**datos_tipo, activo=True)
            guardar_tipo_documento_en_base_de_datos(tipo)

        tipos_listos.append(tipo)

    return tipos_listos


def crear_proveedores_base_si_no_existen():
    """Crea proveedores demo para preparar el modulo de compras."""
    proveedores_listos = []

    for datos_proveedor in PROVEEDORES_BASE:
        numero_documento = datos_proveedor["numero_documento"]
        proveedor = consultar_proveedor_por_documento_en_bd(numero_documento)

        if not proveedor:
            tipo_documento = consultar_tipo_documento_por_codigo_en_bd(
                datos_proveedor["codigo_tipo_documento"],
            )
            proveedor = Proveedor(
                id_tipo_documento=tipo_documento.id_tipo_documento,
                numero_documento=numero_documento,
                nombre=datos_proveedor["nombre"],
                correo=datos_proveedor.get("correo"),
                telefono=datos_proveedor.get("telefono"),
                direccion=datos_proveedor.get("direccion"),
                activo=True,
            )
            guardar_proveedor_en_base_de_datos(proveedor)

        proveedores_listos.append(proveedor)

    return proveedores_listos


def crear_listas_precio_base_si_no_existen():
    """Crea listas de precio demo para preparar ventas."""
    listas_listas = []

    for datos_lista in LISTAS_PRECIO_BASE:
        lista = consultar_lista_precio_por_nombre_en_bd(datos_lista["nombre"])

        if not lista:
            lista = ListaPrecio(**datos_lista)
            guardar_lista_precio_en_base_de_datos(lista)

        listas_listas.append(lista)

    return listas_listas


def crear_precios_producto_base_si_no_existen():
    """Crea precios demo por producto y lista de precio."""
    precios_listos = []

    for datos_precio in PRECIOS_PRODUCTO_BASE:
        producto = consultar_producto_por_codigo_en_bd(datos_precio["codigo_producto"])
        lista = consultar_lista_precio_por_nombre_en_bd(datos_precio["lista_precio"])

        precio = consultar_precio_por_producto_y_lista_en_bd(
            producto.id_producto,
            lista.id_lista_precio,
        )

        if not precio:
            precio = PrecioProducto(
                id_producto=producto.id_producto,
                id_lista_precio=lista.id_lista_precio,
                precio=datos_precio["precio"],
            )
            guardar_precio_producto_en_base_de_datos(precio)

        precios_listos.append(precio)

    return precios_listos


def crear_transportistas_base_si_no_existen():
    """Crea transportistas demo para preparar logistica."""
    transportistas_listos = []

    for datos_transportista in TRANSPORTISTAS_BASE:
        transportista = consultar_transportista_por_identificacion_en_bd(
            datos_transportista["identificacion"]
        )

        if not transportista:
            transportista = Transportista(**datos_transportista)
            guardar_transportista_en_base_de_datos(transportista)

        transportistas_listos.append(transportista)

    return transportistas_listos


def crear_rutas_logistica_base_si_no_existen():
    """Crea rutas logisticas demo entre sucursales reales."""
    rutas_listas = []

    for datos_ruta in RUTAS_LOGISTICA_BASE:
        ruta = consultar_ruta_logistica_por_nombre_en_bd(datos_ruta["nombre_ruta"])

        if not ruta:
            ruta = RutaLogistica(**datos_ruta)
            guardar_ruta_logistica_en_base_de_datos(ruta)

        rutas_listas.append(ruta)

    return rutas_listas


def crear_parametros_sistema_base_si_no_existen():
    """Crea parametros demo de configuracion general."""
    parametros_listos = []

    for datos_parametro in PARAMETROS_SISTEMA_BASE:
        parametro = consultar_parametro_sistema_por_clave_en_bd(datos_parametro["clave"])

        if not parametro:
            parametro = ParametroSistema(**datos_parametro)
            guardar_parametro_sistema_en_base_de_datos(parametro)

        parametros_listos.append(parametro)

    return parametros_listos


def ejecutar_seed_datos_base():
    """Ejecuta todos los datos iniciales que necesita el sistema para arrancar."""
    roles = crear_roles_base_si_no_existen()
    sucursales = crear_sucursales_base_si_no_existen()
    usuarios = crear_usuarios_base_si_no_existen()
    unidades_medida = crear_unidades_medida_base_si_no_existen()
    productos = crear_productos_base_si_no_existen()
    producto_unidades = crear_producto_unidades_base_si_no_existen()
    inventario_sucursal = crear_inventario_sucursal_base_si_no_existe()
    tipos_movimiento_inventario = crear_tipos_movimiento_inventario_base_si_no_existen()
    estados_transferencia = crear_estados_transferencia_base_si_no_existen()
    tipos_documento = crear_tipos_documento_base_si_no_existen()
    proveedores = crear_proveedores_base_si_no_existen()
    listas_precio = crear_listas_precio_base_si_no_existen()
    precios_producto = crear_precios_producto_base_si_no_existen()
    transportistas = crear_transportistas_base_si_no_existen()
    rutas_logistica = crear_rutas_logistica_base_si_no_existen()
    parametros_sistema = crear_parametros_sistema_base_si_no_existen()

    return {
        "roles": roles,
        "sucursales": sucursales,
        "usuarios": usuarios,
        "unidades_medida": unidades_medida,
        "productos": productos,
        "producto_unidades": producto_unidades,
        "inventario_sucursal": inventario_sucursal,
        "tipos_movimiento_inventario": tipos_movimiento_inventario,
        "estados_transferencia": estados_transferencia,
        "tipos_documento": tipos_documento,
        "proveedores": proveedores,
        "listas_precio": listas_precio,
        "precios_producto": precios_producto,
        "transportistas": transportistas,
        "rutas_logistica": rutas_logistica,
        "parametros_sistema": parametros_sistema,
    }
