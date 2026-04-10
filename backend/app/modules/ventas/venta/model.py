from datetime import datetime

from app.extensions import db


class Venta(db.Model):
    """Cabecera de una venta confirmada por una sucursal.

    La venta guarda la informacion general y el comprobante. Los productos
    vendidos viven en detalle_venta para mantener el registro atomico.
    """

    __tablename__ = "venta"

    id_venta = db.Column(db.Integer, primary_key=True)
    id_sucursal = db.Column(db.Integer, db.ForeignKey("sucursales.id_sucursal"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=True)
    id_lista_precio = db.Column(
        db.Integer,
        db.ForeignKey("listas_precio.id_lista_precio"),
        nullable=False,
    )
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descuento_total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    comprobante = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.String(40), nullable=False, default="CONFIRMADA")

    sucursal = db.relationship("Sucursal", lazy=True)
    usuario = db.relationship("Usuario", lazy=True)
    cliente = db.relationship("Cliente", lazy=True)
    lista_precio = db.relationship("ListaPrecio", lazy=True)
    detalles = db.relationship("DetalleVenta", back_populates="venta", lazy=True)

    def convertir_a_diccionario(self, incluir_detalles=True):
        """Devuelve la venta lista para responder por API."""
        respuesta = {
            "id_venta": self.id_venta,
            "id_sucursal": self.id_sucursal,
            "id_usuario": self.id_usuario,
            "id_cliente": self.id_cliente,
            "id_lista_precio": self.id_lista_precio,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "descuento_total": float(self.descuento_total),
            "total": float(self.total),
            "comprobante": self.comprobante,
            "estado": self.estado,
            "cliente": self.cliente.convertir_a_diccionario() if self.cliente else None,
        }

        if incluir_detalles:
            respuesta["detalles"] = [
                detalle.convertir_a_diccionario() for detalle in self.detalles
            ]

        return respuesta
