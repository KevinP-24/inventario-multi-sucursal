from app.extensions import db


class TipoMovimientoInventario(db.Model):
    """Catalogo pequeno con los tipos de movimiento permitidos.

    Lo separamos para no depender de textos quemados en codigo y para mantener
    la base mas atomica y facil de explicar.
    """

    __tablename__ = "tipos_movimiento_inventario"

    id_tipo_movimiento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)

    def convertir_a_diccionario(self):
        """Devuelve el tipo de movimiento listo para responder por API."""
        return {
            "id_tipo_movimiento": self.id_tipo_movimiento,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }
