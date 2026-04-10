from app.extensions import db


class UnidadMedida(db.Model):
    """Representa una unidad en la que se puede medir o vender un producto."""

    __tablename__ = "unidades_medida"

    id_unidad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    simbolo = db.Column(db.String(20), nullable=False, unique=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def convertir_a_diccionario(self):
        """Devuelve la unidad en formato facil de responder por API."""
        return {
            "id_unidad": self.id_unidad,
            "nombre": self.nombre,
            "simbolo": self.simbolo,
            "activo": self.activo,
        }
