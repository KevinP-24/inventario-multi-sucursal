from datetime import date

from app.extensions import db


class PrecioProducto(db.Model):
    """Relaciona un producto con una lista de precio y su valor comercial."""

    __tablename__ = "precios_producto"

    id_precio_producto = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    id_lista_precio = db.Column(db.Integer, db.ForeignKey("listas_precio.id_lista_precio"), nullable=False)
    precio = db.Column(db.Numeric(12, 2), nullable=False)
    fecha_vigencia = db.Column(db.Date, nullable=False, default=date.today)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    producto = db.relationship("Producto", lazy=True)
    lista_precio = db.relationship("ListaPrecio", back_populates="precios")

    __table_args__ = (
        db.UniqueConstraint("id_producto", "id_lista_precio", name="uq_producto_lista_precio"),
    )

    def convertir_a_diccionario(self):
        """Devuelve el precio del producto listo para responder por API."""
        return {
            "id_precio_producto": self.id_precio_producto,
            "id_producto": self.id_producto,
            "id_lista_precio": self.id_lista_precio,
            "precio": float(self.precio),
            "fecha_vigencia": self.fecha_vigencia.isoformat() if self.fecha_vigencia else None,
            "activo": self.activo,
            "producto": self.producto.convertir_a_diccionario() if self.producto else None,
            "lista_precio": self.lista_precio.convertir_a_diccionario() if self.lista_precio else None,
        }
