from app.extensions import db


class Sucursal(db.Model):
    """Representa una sede fisica donde opera el negocio."""

    __tablename__ = "sucursales"

    id_sucursal = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, unique=True)
    direccion = db.Column(db.String(180), nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(30), nullable=True)
    estado = db.Column(db.String(30), nullable=False, default="activa")

    usuarios = db.relationship("Usuario", back_populates="sucursal", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve la sucursal en formato facil de responder por API."""
        return {
            "id_sucursal": self.id_sucursal,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "telefono": self.telefono,
            "estado": self.estado,
        }
