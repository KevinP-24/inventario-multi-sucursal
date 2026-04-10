from app.extensions import db


class EstadoTransferencia(db.Model):
    """Catalogo de estados del ciclo de atencion de una transferencia."""

    __tablename__ = "estados_transferencia"

    id_estado_transferencia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)

    def convertir_a_diccionario(self):
        """Devuelve el estado listo para responder por API."""
        return {
            "id_estado_transferencia": self.id_estado_transferencia,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }
