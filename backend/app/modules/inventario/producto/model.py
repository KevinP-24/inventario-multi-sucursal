from app.extensions import db


class Producto(db.Model):
    """Representa un producto que se puede comprar, vender o inventariar."""

    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    stock_minimo = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    ultimo_costo_compra = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    precio_venta_base = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    unidades = db.relationship("ProductoUnidad", back_populates="producto", lazy=True)
    inventarios = db.relationship("InventarioSucursal", back_populates="producto", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el producto en formato facil de responder por API."""
        stock_total = sum(i.cantidad_actual for i in self.inventarios)
        costo_promedio_global = 0
        if stock_total > 0:
            valor_total = sum(i.cantidad_actual * i.costo_promedio for i in self.inventarios)
            costo_promedio_global = valor_total / stock_total

        return {
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "stock_minimo": float(self.stock_minimo),
            "activo": self.activo,
            "ultimo_costo_compra": float(self.ultimo_costo_compra),
            "precio_venta_base": float(self.precio_venta_base),
            "costo_promedio_global": float(costo_promedio_global),
        }
