from datetime import datetime

from app.extensions import db


class Usuario(db.Model):
    """Representa una persona que puede iniciar sesion en el sistema."""

    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id_rol"), nullable=False)

    # Puede ser NULL para Admin general, porque ese rol tiene alcance global.
    id_sucursal = db.Column(
        db.Integer,
        db.ForeignKey("sucursales.id_sucursal"),
        nullable=True,
    )

    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    rol = db.relationship("Rol", back_populates="usuarios")
    sucursal = db.relationship("Sucursal", back_populates="usuarios")

    def convertir_a_diccionario(self):
        """Devuelve el usuario sin mostrar el password_hash."""
        return {
            "id_usuario": self.id_usuario,
            "id_rol": self.id_rol,
            "id_sucursal": self.id_sucursal,
            "nombre": self.nombre,
            "correo": self.correo,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "rol": self.rol.convertir_a_diccionario() if self.rol else None,
            "sucursal": self.sucursal.convertir_a_diccionario() if self.sucursal else None,
        }
