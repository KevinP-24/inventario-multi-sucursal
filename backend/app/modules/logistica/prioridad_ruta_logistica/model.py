from app.extensions import db


class PrioridadRutaLogistica(db.Model):
    """Catalogo de prioridades permitidas para clasificar rutas logisticas."""

    __tablename__ = "prioridades_ruta_logistica"

    id_prioridad_ruta = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)

    def convertir_a_diccionario(self):
        """Devuelve la prioridad lista para responder por API."""
        return {
            "id_prioridad_ruta": self.id_prioridad_ruta,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }
