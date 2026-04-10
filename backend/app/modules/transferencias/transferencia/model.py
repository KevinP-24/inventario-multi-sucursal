from datetime import datetime

from app.extensions import db


class Transferencia(db.Model):
    """Cabecera del traslado de mercancia entre sucursales.

    Representa el ciclo completo: solicitud, aprobacion, envio y recepcion.
    Los productos solicitados van en detalle_transferencia.
    """

    __tablename__ = "transferencia"

    id_transferencia = db.Column(db.Integer, primary_key=True)
    id_sucursal_origen = db.Column(
        db.Integer,
        db.ForeignKey("sucursales.id_sucursal"),
        nullable=False,
    )
    id_sucursal_destino = db.Column(
        db.Integer,
        db.ForeignKey("sucursales.id_sucursal"),
        nullable=False,
    )
    id_usuario_solicita = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    id_estado_transferencia = db.Column(
        db.Integer,
        db.ForeignKey("estados_transferencia.id_estado_transferencia"),
        nullable=False,
    )
    fecha_solicitud = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prioridad = db.Column(db.String(40), nullable=False, default="NORMAL")
    observacion = db.Column(db.String(255), nullable=True)

    sucursal_origen = db.relationship("Sucursal", foreign_keys=[id_sucursal_origen], lazy=True)
    sucursal_destino = db.relationship("Sucursal", foreign_keys=[id_sucursal_destino], lazy=True)
    usuario_solicita = db.relationship("Usuario", lazy=True)
    estado_transferencia = db.relationship("EstadoTransferencia", lazy=True)
    detalles = db.relationship("DetalleTransferencia", back_populates="transferencia", lazy=True)
    envio = db.relationship("EnvioTransferencia", back_populates="transferencia", uselist=False)
    recepciones = db.relationship("RecepcionTransferencia", back_populates="transferencia", lazy=True)

    def convertir_a_diccionario(self, incluir_detalles=True):
        """Devuelve la transferencia lista para responder por API."""
        respuesta = {
            "id_transferencia": self.id_transferencia,
            "id_sucursal_origen": self.id_sucursal_origen,
            "id_sucursal_destino": self.id_sucursal_destino,
            "id_usuario_solicita": self.id_usuario_solicita,
            "id_estado_transferencia": self.id_estado_transferencia,
            "fecha_solicitud": self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            "prioridad": self.prioridad,
            "estado": self.estado_transferencia.nombre if self.estado_transferencia else None,
            "observacion": self.observacion,
        }

        if incluir_detalles:
            respuesta["detalles"] = [
                detalle.convertir_a_diccionario() for detalle in self.detalles
            ]

        if self.envio:
            respuesta["envio"] = self.envio.convertir_a_diccionario()

        return respuesta
