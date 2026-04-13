from app.extensions import db


class Proveedor(db.Model):
    """Representa una empresa o persona que le vende productos al negocio."""

    __tablename__ = "proveedores"

    id_proveedor = db.Column(db.Integer, primary_key=True)
    id_tipo_documento = db.Column(
        db.Integer,
        db.ForeignKey("tipos_documento.id_tipo_documento"),
        nullable=False,
    )
    numero_documento = db.Column(db.String(40), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    direccion = db.Column(db.String(180), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    tipo_documento = db.relationship("TipoDocumento", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el proveedor en formato facil de responder por API."""
        return {
            "id_proveedor": self.id_proveedor,
            "id_tipo_documento": self.id_tipo_documento,
            "tipo_documento": (
                self.tipo_documento.convertir_a_diccionario()
                if self.tipo_documento else None
            ),
            "numero_documento": self.numero_documento,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "activo": self.activo,
        }
