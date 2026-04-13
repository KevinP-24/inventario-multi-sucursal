from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request


RUTAS_PUBLICAS = {
    "health.",
    "auth.login_endpoint",
    "seed_cli.",
}

PERMISOS_POR_ROL = {
    "Admin general": {"*"},
    "Admin sucursal": {
        "auth",
        "clientes",
        "dashboard",
        "detalles_orden_compra",
        "detalles_transferencia",
        "detalles_venta",
        "estados_transferencia",
        "inventario_sucursal",
        "listas_precio",
        "movimientos_inventario",
        "ordenes_compra",
        "precios_producto",
        "prioridades_ruta_logistica",
        "productos",
        "producto_unidades",
        "proveedores",
        "reportes",
        "rutas_logistica",
        "sucursales",
        "tipos_documento",
        "tipos_movimiento_inventario",
        "transferencias",
        "transportistas",
        "unidades_medida",
        "ventas",
    },
    "Operario de inventario": {
        "auth",
        "clientes",
        "dashboard",
        "detalles_orden_compra",
        "detalles_transferencia",
        "detalles_venta",
        "estados_transferencia",
        "inventario_sucursal",
        "listas_precio",
        "movimientos_inventario",
        "precios_producto",
        "prioridades_ruta_logistica",
        "productos",
        "producto_unidades",
        "proveedores",
        "reportes",
        "rutas_logistica",
        "tipos_documento",
        "tipos_movimiento_inventario",
        "transferencias",
        "transportistas",
        "unidades_medida",
        "ventas",
        "sucursales",
    },
}


def proteger_api_con_jwt(app):
    """Exige JWT y valida rol para endpoints API no publicos."""

    @app.before_request
    def validar_seguridad_api():
        if request.method == "OPTIONS":
            return None

        endpoint = request.endpoint or ""
        if not request.path.startswith("/api/") or es_ruta_publica(endpoint, request.path):
            return None

        try:
            verify_jwt_in_request()
        except Exception as error:
            return jsonify({
                "message": "Token JWT requerido o invalido.",
                "error": str(error),
            }), 401

        claims = get_jwt()
        rol = claims.get("rol")
        blueprint = endpoint.split(".")[0]
        if not rol_tiene_permiso(rol, blueprint):
            return jsonify({
                "message": "El rol no tiene permisos para acceder a este recurso.",
                "rol": rol,
                "recurso": blueprint,
            }), 403

        return None


def roles_requeridos(*roles):
    """Decorador opcional para proteger endpoints con roles especificos."""
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            rol = get_jwt().get("rol")
            if rol not in roles:
                return jsonify({
                    "message": "El rol no tiene permisos para ejecutar esta accion.",
                    "rol": rol,
                }), 403

            return funcion(*args, **kwargs)

        return wrapper

    return decorador


def es_ruta_publica(endpoint, path):
    """Identifica endpoints publicos."""
    return (
        path.startswith("/api/v1/health")
        or any(endpoint == ruta or endpoint.startswith(ruta) for ruta in RUTAS_PUBLICAS)
    )


def rol_tiene_permiso(rol, blueprint):
    rol_normalizado = " ".join((rol or "").split())
    blueprint_normalizado = (blueprint or "").strip()

    permisos = PERMISOS_POR_ROL.get(rol_normalizado, set())

    print("DEBUG rol:", repr(rol))
    print("DEBUG rol_normalizado:", repr(rol_normalizado))
    print("DEBUG blueprint:", repr(blueprint_normalizado))
    print("DEBUG permisos:", permisos)

    return "*" in permisos or blueprint_normalizado in permisos