import os
from flask import Flask

from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors
from app.api.health import health_bp

def create_app():
    config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")

    return app