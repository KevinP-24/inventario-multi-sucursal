from app.extensions import db


class Rol(db.Model):
    """Representa los actores/perfiles que pueden usar el sistema."""

    __tablename__ = "roles"

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    usuarios = db.relationship("Usuario", back_populates="rol", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el rol en formato facil de convertir a JSON."""
        return {
            "id_rol": self.id_rol,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }
