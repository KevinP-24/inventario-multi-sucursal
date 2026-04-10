from datetime import datetime

from app.extensions import db


class EnvioTransferencia(db.Model):
    """Despacho logistico asociado a una transferencia aprobada."""

    __tablename__ = "envio_transferencia"

    id_envio = db.Column(db.Integer, primary_key=True)
    id_transferencia = db.Column(
        db.Integer,
        db.ForeignKey("transferencia.id_transferencia"),
        nullable=False,
        unique=True,
    )
    id_ruta = db.Column(db.Integer, db.ForeignKey("rutas_logistica.id_ruta"), nullable=False)
    id_transportista = db.Column(
        db.Integer,
        db.ForeignKey("transportistas.id_transportista"),
        nullable=False,
    )
    fecha_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_estimada_llegada = db.Column(db.DateTime, nullable=True)
    fecha_real_llegada = db.Column(db.DateTime, nullable=True)
    estado_envio = db.Column(db.String(40), nullable=False, default="EN_TRANSITO")

    transferencia = db.relationship("Transferencia", back_populates="envio", lazy=True)
    ruta = db.relationship("RutaLogistica", lazy=True)
    transportista = db.relationship("Transportista", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el envio listo para responder por API."""
        return {
            "id_envio": self.id_envio,
            "id_transferencia": self.id_transferencia,
            "id_ruta": self.id_ruta,
            "id_transportista": self.id_transportista,
            "fecha_envio": self.fecha_envio.isoformat() if self.fecha_envio else None,
            "fecha_estimada_llegada": (
                self.fecha_estimada_llegada.isoformat() if self.fecha_estimada_llegada else None
            ),
            "fecha_real_llegada": (
                self.fecha_real_llegada.isoformat() if self.fecha_real_llegada else None
            ),
            "estado_envio": self.estado_envio,
        }
