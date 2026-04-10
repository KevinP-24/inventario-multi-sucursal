from app.extensions import db


class IncidenciaTransferencia(db.Model):
    """Diferencia o faltante detectado en una recepcion parcial."""

    __tablename__ = "incidencia_transferencia"

    id_incidencia = db.Column(db.Integer, primary_key=True)
    id_recepcion = db.Column(
        db.Integer,
        db.ForeignKey("recepcion_transferencia.id_recepcion"),
        nullable=False,
    )
    id_detalle_transferencia = db.Column(
        db.Integer,
        db.ForeignKey("detalle_transferencia.id_detalle_transferencia"),
        nullable=False,
    )
    cantidad_faltante = db.Column(db.Numeric(12, 2), nullable=False)
    tratamiento = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    recepcion = db.relationship("RecepcionTransferencia", back_populates="incidencias", lazy=True)
    detalle_transferencia = db.relationship("DetalleTransferencia", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve la incidencia lista para responder por API."""
        return {
            "id_incidencia": self.id_incidencia,
            "id_recepcion": self.id_recepcion,
            "id_detalle_transferencia": self.id_detalle_transferencia,
            "cantidad_faltante": float(self.cantidad_faltante),
            "tratamiento": self.tratamiento,
            "descripcion": self.descripcion,
        }
