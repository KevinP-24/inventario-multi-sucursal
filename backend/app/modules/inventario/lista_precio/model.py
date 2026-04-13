from app.extensions import db


class ListaPrecio(db.Model):
    """Representa una lista comercial para vender con diferentes precios."""

    __tablename__ = "listas_precio"

    id_lista_precio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)
    activa = db.Column(db.Boolean, nullable=False, default=True)

    precios = db.relationship("PrecioProducto", back_populates="lista_precio", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve la lista de precio lista para responder por API."""
        return {
            "id_lista_precio": self.id_lista_precio,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activa": self.activa,
        }
