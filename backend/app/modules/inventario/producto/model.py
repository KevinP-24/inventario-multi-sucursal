from app.extensions import db


class Producto(db.Model):
    """Representa un producto que se puede comprar, vender o inventariar."""

    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    stock_minimo = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def convertir_a_diccionario(self):
        """Devuelve el producto en formato facil de responder por API."""
        return {
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "stock_minimo": float(self.stock_minimo),
            "activo": self.activo,
        }
