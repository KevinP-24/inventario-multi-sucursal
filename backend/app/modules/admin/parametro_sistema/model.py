from app.extensions import db


class ParametroSistema(db.Model):
    """Representa una configuracion simple del sistema."""

    __tablename__ = "parametros_sistema"

    id_parametro = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(120), nullable=False, unique=True)
    valor = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def convertir_a_diccionario(self):
        """Devuelve el parametro listo para responder por API."""
        return {
            "id_parametro": self.id_parametro,
            "clave": self.clave,
            "valor": self.valor,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }
