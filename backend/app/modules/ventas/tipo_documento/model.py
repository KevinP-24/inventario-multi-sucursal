from app.extensions import db


class TipoDocumento(db.Model):
    """Catalogo de documentos de identificacion usados para clientes."""

    __tablename__ = "tipos_documento"

    id_tipo_documento = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False, unique=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def convertir_a_diccionario(self):
        """Devuelve el tipo de documento listo para API."""
        return {
            "id_tipo_documento": self.id_tipo_documento,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }
