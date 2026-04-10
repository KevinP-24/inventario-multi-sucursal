from flask import Blueprint, jsonify, request

from app.modules.auth.rol.service import (
    actualizar_rol_con_validaciones,
    crear_rol_con_validaciones,
    crear_roles_base_si_no_existen,
    listar_roles_para_respuesta,
    obtener_rol_para_respuesta,
)

roles_bp = Blueprint("roles", __name__)


@roles_bp.get("/listar_roles")
def listar_roles_endpoint():
    """Lista todos los roles disponibles."""
    return jsonify({"data": listar_roles_para_respuesta()}), 200


@roles_bp.get("/obtener_rol/<int:id_rol>")
def obtener_rol_endpoint(id_rol):
    """Consulta un rol por id."""
    rol = obtener_rol_para_respuesta(id_rol)
    if not rol:
        return jsonify({"message": "Rol no encontrado."}), 404

    return jsonify({"data": rol}), 200


@roles_bp.post("/crear_rol")
def crear_rol_endpoint():
    """Crea un rol nuevo."""
    datos = request.get_json(silent=True) or {}
    rol, errores = crear_rol_con_validaciones(datos)

    if errores:
        return jsonify({"message": "No se pudo crear el rol.", "errors": errores}), 400

    return jsonify({"message": "Rol creado correctamente.", "data": rol}), 201


@roles_bp.put("/actualizar_rol/<int:id_rol>")
def actualizar_rol_endpoint(id_rol):
    """Actualiza un rol existente."""
    datos = request.get_json(silent=True) or {}
    rol, errores = actualizar_rol_con_validaciones(id_rol, datos)

    if errores:
        return jsonify({"message": "No se pudo actualizar el rol.", "errors": errores}), 400

    return jsonify({"message": "Rol actualizado correctamente.", "data": rol}), 200


@roles_bp.post("/crear_roles_base")
def crear_roles_base_endpoint():
    """Crea los tres roles principales usados por los actores del sistema."""
    roles = crear_roles_base_si_no_existen()
    return jsonify({"message": "Roles base listos.", "data": roles}), 200
