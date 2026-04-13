from app.extensions import db


class InventarioSucursal(db.Model):
    """Stock actual de un producto en una sucursal.

    Esta tabla es el puente entre producto y sucursal. Aqui no guardamos el
    historial; el historial va despues en movimiento_inventario.
    """

    __tablename__ = "inventario_sucursal"

    id_inventario = db.Column(db.Integer, primary_key=True)
    id_sucursal = db.Column(db.Integer, db.ForeignKey("sucursales.id_sucursal"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    cantidad_actual = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    costo_promedio = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    __table_args__ = (
        db.UniqueConstraint("id_sucursal", "id_producto", name="uq_inventario_sucursal_producto"),
    )

    sucursal = db.relationship("Sucursal", lazy=True)
    producto = db.relationship("Producto", back_populates="inventarios", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el inventario en formato facil de leer por API."""
        return {
            "id_inventario": self.id_inventario,
            "id_sucursal": self.id_sucursal,
            "id_producto": self.id_producto,
            "cantidad_actual": float(self.cantidad_actual),
            "costo_promedio": float(self.costo_promedio),
        }
