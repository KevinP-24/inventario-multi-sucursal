from datetime import datetime

from app.extensions import db


class MovimientoInventario(db.Model):
    """Historial de cambios del inventario.

    Esta tabla explica por que cambio el stock. El stock actual vive en
    inventario_sucursal; aqui dejamos la trazabilidad de cada entrada o salida.
    """

    __tablename__ = "movimientos_inventario"

    id_movimiento = db.Column(db.Integer, primary_key=True)
    id_inventario = db.Column(
        db.Integer,
        db.ForeignKey("inventario_sucursal.id_inventario"),
        nullable=False,
    )
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    id_tipo_movimiento = db.Column(
        db.Integer,
        db.ForeignKey("tipos_movimiento_inventario.id_tipo_movimiento"),
        nullable=False,
    )
    motivo = db.Column(db.String(255), nullable=True)
    cantidad = db.Column(db.Numeric(12, 2), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modulo_origen = db.Column(db.String(80), nullable=True)
    id_origen = db.Column(db.Integer, nullable=True)

    inventario = db.relationship("InventarioSucursal", lazy=True)
    usuario = db.relationship("Usuario", lazy=True)
    tipo_movimiento = db.relationship("TipoMovimientoInventario", lazy=True)

    def convertir_a_diccionario(self):
        """Devuelve el movimiento listo para responder por API."""
        return {
            "id_movimiento": self.id_movimiento,
            "id_inventario": self.id_inventario,
            "id_usuario": self.id_usuario,
            "id_tipo_movimiento": self.id_tipo_movimiento,
            "tipo_movimiento": self.tipo_movimiento.nombre if self.tipo_movimiento else None,
            "motivo": self.motivo,
            "cantidad": float(self.cantidad),
            "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "modulo_origen": self.modulo_origen,
            "id_origen": self.id_origen,
        }
