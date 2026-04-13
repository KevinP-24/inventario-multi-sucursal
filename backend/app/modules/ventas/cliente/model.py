from datetime import datetime

from app.extensions import db


class Cliente(db.Model):
    """Representa a la persona o empresa a la que se le vende."""

    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    id_tipo_documento = db.Column(
        db.Integer,
        db.ForeignKey("tipos_documento.id_tipo_documento"),
        nullable=False,
    )
    numero_documento = db.Column(db.String(40), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    tipo_documento = db.relationship("TipoDocumento", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el cliente listo para responder por JSON."""
        return {
            "id_cliente": self.id_cliente,
            "id_tipo_documento": self.id_tipo_documento,
            "tipo_documento": (
                self.tipo_documento.convertir_a_diccionario()
                if self.tipo_documento else None
            ),
            "numero_documento": self.numero_documento,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
