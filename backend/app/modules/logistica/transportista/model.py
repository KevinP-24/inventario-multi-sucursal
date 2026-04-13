from app.extensions import db


class Transportista(db.Model):
    """Representa quien puede transportar mercancia entre sucursales."""

    __tablename__ = "transportistas"

    id_transportista = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(40), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(30), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def convertir_a_diccionario(self):
        """Devuelve el transportista listo para responder por API."""
        return {
            "id_transportista": self.id_transportista,
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "activo": self.activo,
        }
