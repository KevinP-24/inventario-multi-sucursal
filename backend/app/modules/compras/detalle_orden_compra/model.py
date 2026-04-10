from app.extensions import db


class DetalleOrdenCompra(db.Model):
    """Producto incluido dentro de una orden de compra.

    Cada fila responde: que producto se compra, en que unidad, cuanto cuesta y
    cuanto aporta al subtotal de la orden.
    """

    __tablename__ = "detalle_orden_compra"

    id_detalle_oc = db.Column(db.Integer, primary_key=True)
    id_orden_compra = db.Column(
        db.Integer,
        db.ForeignKey("orden_compra.id_orden_compra"),
        nullable=False,
    )
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

    orden_compra = db.relationship("OrdenCompra", back_populates="detalles", lazy=True)
    producto = db.relationship("Producto", lazy=True)
    producto_unidad = db.relationship("ProductoUnidad", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el detalle listo para responder por API."""
        return {
            "id_detalle_oc": self.id_detalle_oc,
            "id_orden_compra": self.id_orden_compra,
            "id_producto": self.id_producto,
            "id_producto_unidad": self.id_producto_unidad,
            "cantidad": float(self.cantidad),
            "precio_unitario": float(self.precio_unitario),
            "descuento": float(self.descuento),
            "subtotal": float(self.subtotal),
        }
