from app.extensions import db


class ProductoUnidad(db.Model):
    """Relaciona un producto con una unidad de medida y su conversion."""

    __tablename__ = "producto_unidades"

    id_producto_unidad = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    id_unidad = db.Column(db.Integer, db.ForeignKey("unidades_medida.id_unidad"), nullable=False)
    factor_conversion = db.Column(db.Numeric(12, 4), nullable=False, default=1)
    es_base = db.Column(db.Boolean, nullable=False, default=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    producto = db.relationship("Producto", back_populates="unidades")
    unidad_medida = db.relationship("UnidadMedida", back_populates="productos")

    __table_args__ = (
        db.UniqueConstraint("id_producto", "id_unidad", name="uq_producto_unidad"),
    )

    def convertir_a_diccionario(self):
        """Devuelve la relacion producto-unidad lista para responder por API."""
        return {
            "id_producto_unidad": self.id_producto_unidad,
            "id_producto": self.id_producto,
            "id_unidad": self.id_unidad,
            "factor_conversion": float(self.factor_conversion),
            "es_base": self.es_base,
            "activo": self.activo,
            "producto": self.producto.convertir_a_diccionario() if self.producto else None,
            "unidad_medida": self.unidad_medida.convertir_a_diccionario() if self.unidad_medida else None,
        }
