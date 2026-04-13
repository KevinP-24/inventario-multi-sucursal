from datetime import datetime

from app.extensions import db


class RecepcionTransferencia(db.Model):
    """Registro de recepcion completa o parcial en la sucursal destino."""

    __tablename__ = "recepcion_transferencia"

    id_recepcion = db.Column(db.Integer, primary_key=True)
    id_transferencia = db.Column(
        db.Integer,
        db.ForeignKey("transferencia.id_transferencia"),
        nullable=False,
    )
    id_usuario_recibe = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_recepcion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo_recepcion = db.Column(db.String(40), nullable=False)
    observacion = db.Column(db.String(255), nullable=True)

    transferencia = db.relationship("Transferencia", back_populates="recepciones", lazy=True)
    usuario_recibe = db.relationship("Usuario", lazy=True)
    incidencias = db.relationship("IncidenciaTransferencia", back_populates="recepcion", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve la recepcion lista para responder por API."""
        return {
            "id_recepcion": self.id_recepcion,
            "id_transferencia": self.id_transferencia,
            "id_usuario_recibe": self.id_usuario_recibe,
            "fecha_recepcion": self.fecha_recepcion.isoformat() if self.fecha_recepcion else None,
            "tipo_recepcion": self.tipo_recepcion,
            "observacion": self.observacion,
            "incidencias": [
                incidencia.convertir_a_diccionario() for incidencia in self.incidencias
            ],
        }
