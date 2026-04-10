from app.extensions import db


class RutaLogistica(db.Model):
    """Representa una ruta logistica segun el diagrama E-R.

    Ojo: esta tabla solo describe la ruta. La relacion entre sucursal origen y
    sucursal destino pertenece a la transferencia, no a esta entidad.
    """

    __tablename__ = "rutas_logistica"

    id_ruta = db.Column(db.Integer, primary_key=True)
    nombre_ruta = db.Column(db.String(120), nullable=False, unique=True)
    id_prioridad_ruta = db.Column(
        db.Integer,
        db.ForeignKey("prioridades_ruta_logistica.id_prioridad_ruta"),
        nullable=False,
    )
    costo_estimado = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    tiempo_estimado = db.Column(db.String(80), nullable=True)

    prioridad_ruta = db.relationship("PrioridadRutaLogistica", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve la ruta logistica lista para responder por API."""
        return {
            "id_ruta": self.id_ruta,
            "nombre_ruta": self.nombre_ruta,
            "id_prioridad_ruta": self.id_prioridad_ruta,
            "prioridad": self.prioridad_ruta.nombre if self.prioridad_ruta else None,
            "costo_estimado": float(self.costo_estimado),
            "tiempo_estimado": self.tiempo_estimado,
        }
