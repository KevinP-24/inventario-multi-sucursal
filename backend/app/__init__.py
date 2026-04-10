import os
from flask import Flask

from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors
from app.api.health import health_bp
from app.modules.auth import roles_bp, usuarios_bp
from app.modules.inventario import productos_bp, unidades_medida_bp
from app.modules.sucursales import sucursales_bp
from app.modules.ventas import clientes_bp
from app.database.seeders import seed_cli

# Cargamos los modelos que ya existen para que las migraciones los detecten.
from app.database import base  # noqa: F401


def create_app():
    config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL is not configured for the Flask application.")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(roles_bp, url_prefix="/api/v1/roles")
    app.register_blueprint(usuarios_bp, url_prefix="/api/v1/usuarios")
    app.register_blueprint(sucursales_bp, url_prefix="/api/v1/sucursales")
    app.register_blueprint(clientes_bp, url_prefix="/api/v1/clientes")
    app.register_blueprint(unidades_medida_bp, url_prefix="/api/v1/unidades-medida")
    app.register_blueprint(productos_bp, url_prefix="/api/v1/productos")
    app.register_blueprint(seed_cli)

    return app
