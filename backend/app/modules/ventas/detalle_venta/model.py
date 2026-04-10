from app.extensions import db


class DetalleVenta(db.Model):
    """Producto vendido dentro de una venta.

    Cada fila conserva el producto, la unidad usada en la venta, la cantidad,
    el precio aplicado desde la lista de precios y el descuento.
    """

    __tablename__ = "detalle_venta"

    id_detalle_venta = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey("venta.id_venta"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    id_producto_unidad = db.Column(
        db.Integer,
        db.ForeignKey("producto_unidades.id_producto_unidad"),
        nullable=False,
    )
    cantidad = db.Column(db.Numeric(12, 2), nullable=False)
    precio_unitario = db.Column(db.Numeric(12, 2), nullable=False)
    descuento = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    venta = db.relationship("Venta", back_populates="detalles", lazy=True)
    producto = db.relationship("Producto", lazy=True)
    producto_unidad = db.relationship("ProductoUnidad", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el detalle listo para responder por API."""
        return {
            "id_detalle_venta": self.id_detalle_venta,
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "id_producto_unidad": self.id_producto_unidad,
            "cantidad": float(self.cantidad),
            "precio_unitario": float(self.precio_unitario),
            "descuento": float(self.descuento),
            "subtotal": float(self.subtotal),
        }
