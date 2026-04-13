from app.extensions import db


class DetalleTransferencia(db.Model):
    """Producto solicitado, aprobado y recibido dentro de una transferencia."""

    __tablename__ = "detalle_transferencia"

    id_detalle_transferencia = db.Column(db.Integer, primary_key=True)
    id_transferencia = db.Column(
        db.Integer,
        db.ForeignKey("transferencia.id_transferencia"),
        nullable=False,
    )
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    id_producto_unidad = db.Column(
        db.Integer,
        db.ForeignKey("producto_unidades.id_producto_unidad"),
        nullable=False,
    )
    cantidad_solicitada = db.Column(db.Numeric(12, 2), nullable=False)
    cantidad_aprobada = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    cantidad_recibida = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    transferencia = db.relationship("Transferencia", back_populates="detalles", lazy=True)
    producto = db.relationship("Producto", lazy=True)
    producto_unidad = db.relationship("ProductoUnidad", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el detalle listo para responder por API."""
        return {
            "id_detalle_transferencia": self.id_detalle_transferencia,
            "id_transferencia": self.id_transferencia,
            "id_producto": self.id_producto,
            "id_producto_unidad": self.id_producto_unidad,
            "cantidad_solicitada": float(self.cantidad_solicitada),
            "cantidad_aprobada": float(self.cantidad_aprobada),
            "cantidad_recibida": float(self.cantidad_recibida),
        }
