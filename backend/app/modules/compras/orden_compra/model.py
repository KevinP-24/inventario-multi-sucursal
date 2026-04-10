from datetime import date

from app.extensions import db


class OrdenCompra(db.Model):
    """Cabecera de una compra hecha a un proveedor.

    La orden guarda los datos generales y los totales. Los productos comprados
    van en detalle_orden_compra para mantener la tabla atomica.
    """

    __tablename__ = "orden_compra"

    id_orden_compra = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey("proveedores.id_proveedor"), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey("sucursales.id_sucursal"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    estado = db.Column(db.String(40), nullable=False, default="CREADA")
    plazo_pago = db.Column(db.String(80), nullable=True)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    descuento_total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    fecha_recepcion = db.Column(db.Date, nullable=True)
    id_usuario_recepcion = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=True)

    proveedor = db.relationship("Proveedor", lazy=True)
    sucursal = db.relationship("Sucursal", lazy=True)
    usuario = db.relationship("Usuario", foreign_keys=[id_usuario], lazy=True)
    usuario_recepcion = db.relationship("Usuario", foreign_keys=[id_usuario_recepcion], lazy=True)
    detalles = db.relationship("DetalleOrdenCompra", back_populates="orden_compra", lazy=True)

    def convertir_a_diccionario(self, incluir_detalles=True):
        """Devuelve la orden lista para responder por API."""
        respuesta = {
            "id_orden_compra": self.id_orden_compra,
            "id_proveedor": self.id_proveedor,
            "id_sucursal": self.id_sucursal,
            "id_usuario": self.id_usuario,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "estado": self.estado,
            "plazo_pago": self.plazo_pago,
            "subtotal": float(self.subtotal),
            "descuento_total": float(self.descuento_total),
            "total": float(self.total),
            "fecha_recepcion": self.fecha_recepcion.isoformat() if self.fecha_recepcion else None,
            "id_usuario_recepcion": self.id_usuario_recepcion,
        }

        if incluir_detalles:
            respuesta["detalles"] = [
                detalle.convertir_a_diccionario() for detalle in self.detalles
            ]

        return respuesta
